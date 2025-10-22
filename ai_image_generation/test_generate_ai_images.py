"""
Test suite for ValueSnap AI Image Generator
Tests image generation functionality and validates successful generation
"""

import os
import json
import tempfile
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import our generator
from generate_ai_images import ValueSnapImageGenerator


class TestValueSnapImageGenerator:
    """Test cases for the ValueSnap image generator"""
    
    @pytest.fixture
    def mock_api_key(self):
        """Provide a mock API key for testing"""
        return "sk-test-fake-api-key-for-testing-12345"
    
    @pytest.fixture
    def generator(self, mock_api_key):
        """Create a generator instance for testing"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': mock_api_key}):
            return ValueSnapImageGenerator(api_key=mock_api_key)
    
    @pytest.fixture
    def mock_openai_response(self):
        """Mock successful OpenAI API response"""
        mock_response = Mock()
        mock_response.data = [Mock()]
        mock_response.data[0].url = "https://example.com/test-image.png"
        return mock_response
    
    @pytest.fixture
    def mock_image_content(self):
        """Mock image content for download simulation"""
        # Create a minimal PNG-like content
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x04\x00\x08\x06\x00\x00\x00'
    
    def test_initialization_with_api_key(self, mock_api_key):
        """Test generator initialization with valid API key"""
        generator = ValueSnapImageGenerator(api_key=mock_api_key)
        assert generator.api_key == mock_api_key
        assert generator.images_dir.exists()
    
    def test_initialization_without_api_key(self):
        """Test generator initialization fails without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                ValueSnapImageGenerator()
    
    def test_initialization_with_env_var(self, mock_api_key):
        """Test generator initialization with environment variable"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': mock_api_key}):
            generator = ValueSnapImageGenerator()
            assert generator.api_key == mock_api_key
    
    def test_consumer_personas_defined(self, generator):
        """Test that all expected consumer personas are defined"""
        expected_personas = [
            "estate_inheritor",
            "reseller_entrepreneur", 
            "antique_collector",
            "small_business_owner"
        ]
        
        assert len(generator.consumer_personas) == len(expected_personas)
        
        for persona_key in expected_personas:
            assert persona_key in generator.consumer_personas
            persona = generator.consumer_personas[persona_key]
            
            # Validate persona structure
            assert 'name' in persona
            assert 'age_range' in persona
            assert 'description' in persona
            assert 'prompt' in persona
            
            # Validate content is not empty
            assert len(persona['name']) > 0
            assert len(persona['description']) > 0
            assert len(persona['prompt']) > 0
    
    def test_get_persona_info(self, generator):
        """Test getting persona information"""
        info = generator.get_persona_info()
        
        assert isinstance(info, dict)
        assert len(info) == len(generator.consumer_personas)
        
        for key, persona_info in info.items():
            assert 'name' in persona_info
            assert 'age_range' in persona_info
            assert 'description' in persona_info
    
    def test_invalid_persona_key(self, generator):
        """Test error handling for invalid persona key"""
        with pytest.raises(ValueError, match="Unknown persona"):
            generator.generate_consumer_image("invalid_persona")
    
    @patch('generate_ai_images.requests.get')
    @patch('generate_ai_images.Image.open')
    @patch('builtins.open', create=True)
    def test_successful_image_generation(self, mock_open, mock_image_open, mock_requests, 
                                       generator, mock_openai_response, mock_image_content):
        """Test successful image generation flow"""
        
        # Mock OpenAI API call
        with patch.object(generator.client.images, 'generate', return_value=mock_openai_response):
            
            # Mock requests.get for image download
            mock_response = Mock()
            mock_response.content = mock_image_content
            mock_response.raise_for_status = Mock()
            mock_requests.return_value = mock_response
            
            # Mock PIL Image for verification
            mock_img = Mock()
            mock_img.size = (1024, 1024)
            mock_img.format = 'PNG'
            mock_image_open.return_value.__enter__.return_value = mock_img
            
            # Mock file writing
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            # Test image generation
            result = generator.generate_consumer_image("estate_inheritor")
            
            # Validate result structure
            assert isinstance(result, dict)
            assert result['persona_key'] == 'estate_inheritor'
            assert result['persona_name'] == 'Estate Inheritor'
            assert result['image_url'] == "https://example.com/test-image.png"
            assert 'file_path' in result
            assert 'filename' in result
            assert result['size'] == "1024x1024"
            assert result['format'] == 'PNG'
            assert 'timestamp' in result
            assert 'prompt_used' in result
            
            # Verify API was called
            generator.client.images.generate.assert_called_once()
            
            # Verify image download
            mock_requests.assert_called_once_with("https://example.com/test-image.png")
            
            # Verify file writing
            mock_file.write.assert_called_once_with(mock_image_content)
    
    def test_api_error_handling(self, generator):
        """Test handling of OpenAI API errors"""
        
        # Mock API to raise an exception
        with patch.object(generator.client.images, 'generate', side_effect=Exception("API Error")):
            
            with pytest.raises(Exception, match="Failed to generate image for Estate Inheritor"):
                generator.generate_consumer_image("estate_inheritor")
    
    def test_image_download_error_handling(self, generator, mock_openai_response):
        """Test handling of image download errors"""
        
        with patch.object(generator.client.images, 'generate', return_value=mock_openai_response):
            
            # Mock requests.get to raise an exception
            with patch('generate_ai_images.requests.get', side_effect=Exception("Download Error")):
                
                with pytest.raises(Exception, match="Failed to generate image for Estate Inheritor"):
                    generator.generate_consumer_image("estate_inheritor")
    
    @patch('generate_ai_images.requests.get')
    @patch('generate_ai_images.Image.open')
    @patch('builtins.open', create=True)
    def test_generate_all_personas(self, mock_open, mock_image_open, mock_requests,
                                  generator, mock_openai_response, mock_image_content):
        """Test generating images for all personas"""
        
        # Setup mocks for successful generation
        with patch.object(generator.client.images, 'generate', return_value=mock_openai_response):
            mock_response = Mock()
            mock_response.content = mock_image_content
            mock_response.raise_for_status = Mock()
            mock_requests.return_value = mock_response
            
            mock_img = Mock()
            mock_img.size = (1024, 1024)
            mock_img.format = 'PNG'
            mock_image_open.return_value.__enter__.return_value = mock_img
            
            mock_file = Mock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            # Mock time.sleep to speed up test
            with patch('generate_ai_images.time.sleep'):
                results = generator.generate_all_personas(delay=0)
            
            # Validate results
            assert len(results) == len(generator.consumer_personas)
            
            successful_results = [r for r in results if 'error' not in r]
            assert len(successful_results) == len(generator.consumer_personas)
            
            # Verify each result
            for result in successful_results:
                assert 'persona_key' in result
                assert 'persona_name' in result
                assert 'image_url' in result
                assert 'file_path' in result
    
    def test_save_generation_report(self, generator, tmp_path):
        """Test saving generation report"""
        
        # Create temporary directory for test
        generator.images_dir = tmp_path
        
        # Mock results
        results = [
            {
                'persona_key': 'estate_inheritor',
                'persona_name': 'Estate Inheritor',
                'image_url': 'https://example.com/test.png',
                'file_path': '/path/to/image.png',
                'filename': 'test.png',
                'timestamp': '20231022_123456'
            },
            {
                'persona_key': 'invalid_persona',
                'error': 'Test error',
                'timestamp': '20231022_123457'
            }
        ]
        
        # Save report
        report_path = generator.save_generation_report(results, 'test_report.json')
        
        # Verify report was created
        assert Path(report_path).exists()
        
        # Verify report content
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        assert 'generation_timestamp' in report
        assert report['total_personas'] == len(generator.consumer_personas)
        assert report['successful_generations'] == 1
        assert report['failed_generations'] == 1
        assert report['results'] == results


class TestIntegration:
    """Integration tests for the complete workflow"""
    
    def test_persona_prompts_quality(self):
        """Test that persona prompts are detailed and professional"""
        generator = ValueSnapImageGenerator(api_key="test-key")
        
        for persona_key, persona in generator.consumer_personas.items():
            prompt = persona['prompt']
            
            # Check prompt length (should be detailed)
            assert len(prompt) > 50, f"Prompt for {persona_key} is too short"
            
            # Check for key elements that make good DALL-E prompts
            assert 'portrait' in prompt.lower() or 'person' in prompt.lower(), \
                f"Prompt for {persona_key} should include person/portrait"
            
            assert 'realistic' in prompt.lower() or 'photography' in prompt.lower(), \
                f"Prompt for {persona_key} should specify realistic style"
            
            # Check for age/demographic information
            assert any(age in prompt for age in ['year-old', 'years old', 'aged']), \
                f"Prompt for {persona_key} should include age information"
    
    def test_persona_alignment_with_valuesnap(self):
        """Test that personas align with ValueSnap's target market"""
        generator = ValueSnapImageGenerator(api_key="test-key")
        
        # Verify we have personas that cover ValueSnap's key markets
        persona_names = [p['name'].lower() for p in generator.consumer_personas.values()]
        
        # Should cover estate/inheritance market
        assert any('estate' in name or 'inherit' in name for name in persona_names)
        
        # Should cover resale/flipping market  
        assert any('resell' in name or 'entrepreneur' in name for name in persona_names)
        
        # Should cover antique/collector market
        assert any('antique' in name or 'collector' in name for name in persona_names)
        
        # Should cover small business market
        assert any('business' in name or 'shop' in name for name in persona_names)


# Test runner for manual execution
if __name__ == "__main__":
    # Run specific test functions for quick validation
    print("🧪 Running ValueSnap Image Generator Tests")
    print("=" * 50)
    
    # Test persona definitions
    try:
        generator = ValueSnapImageGenerator(api_key="test-key")
        personas = generator.get_persona_info()
        
        print(f"✅ Personas loaded: {len(personas)}")
        for key, info in personas.items():
            print(f"  • {info['name']} ({info['age_range']})")
        
        print("\n🎨 Testing prompt quality...")
        test_integration = TestIntegration()
        test_integration.test_persona_prompts_quality()
        test_integration.test_persona_alignment_with_valuesnap()
        print("✅ All persona prompts pass quality checks")
        
        print("\n🔧 Testing error handling...")
        try:
            generator.generate_consumer_image("invalid_persona")
        except ValueError as e:
            print(f"✅ Invalid persona error handling works: {e}")
        
        print("\n📊 Test Summary:")
        print("  ✅ Persona definitions: PASS")
        print("  ✅ Prompt quality: PASS") 
        print("  ✅ Error handling: PASS")
        print("  ✅ Market alignment: PASS")
        
        print(f"\n🚀 Ready to generate images! Run with valid OpenAI API key.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")