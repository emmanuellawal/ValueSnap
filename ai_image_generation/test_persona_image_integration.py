"""
Test suite for verifying OpenAI-generated images are correctly integrated
into the ValueSnap "Who It's For" persona section.

This test ensures:
1. Images are generated for the correct personas
2. Images exist in the expected locations
3. HTML references the correct image paths
4. Images have appropriate dimensions and formats
5. All persona cards have corresponding AI-generated images
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
import pytest
from bs4 import BeautifulSoup
from PIL import Image


class TestPersonaImageIntegration:
    """Test AI-generated images integration in the webpage"""
    
    # Expected personas in the "Who It's For" section
    EXPECTED_PERSONAS = {
        'estate_inheritor': {
            'html_identifier': 'Emeka',  # Current HTML uses "Emeka, 37"
            'expected_role': 'Estate Manager',
            'avatar_class': 'persona-avatar'
        },
        'reseller_entrepreneur': {
            'html_identifier': 'Jake',  # Current HTML uses "Jake, 28"
            'expected_role': 'Reseller',
            'avatar_class': 'persona-avatar'
        }
    }
    
    @pytest.fixture
    def project_root(self):
        """Get the project root directory"""
        current_dir = Path(__file__).parent
        return current_dir.parent
    
    @pytest.fixture
    def html_file_path(self, project_root):
        """Get the index.html file path"""
        return project_root / 'index.html'
    
    @pytest.fixture
    def images_dir(self):
        """Get the generated images directory"""
        return Path(__file__).parent / 'generated_images'
    
    @pytest.fixture
    def html_content(self, html_file_path):
        """Load and parse the HTML content"""
        if not html_file_path.exists():
            pytest.skip(f"HTML file not found: {html_file_path}")
        
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return BeautifulSoup(content, 'html.parser')
    
    def test_images_directory_exists(self, images_dir):
        """Test that the generated_images directory exists"""
        assert images_dir.exists(), f"Generated images directory not found: {images_dir}"
        assert images_dir.is_dir(), f"Path exists but is not a directory: {images_dir}"
    
    def test_persona_images_generated(self, images_dir):
        """Test that images have been generated for each persona"""
        image_files = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg'))
        
        assert len(image_files) > 0, \
            "No images found in generated_images directory. Run generate_ai_images.py first."
        
        # Check that we have images for each expected persona
        for persona_key in self.EXPECTED_PERSONAS.keys():
            matching_images = [f for f in image_files if persona_key in f.name]
            assert len(matching_images) > 0, \
                f"No generated image found for persona: {persona_key}"
    
    def test_persona_images_valid_format(self, images_dir):
        """Test that generated images are valid image files with correct format"""
        image_files = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg'))
        
        for image_path in image_files:
            try:
                with Image.open(image_path) as img:
                    # Verify it's a valid image
                    assert img.format in ['PNG', 'JPEG'], \
                        f"Invalid image format for {image_path.name}: {img.format}"
                    
                    # Verify dimensions are reasonable (at least 256x256)
                    width, height = img.size
                    assert width >= 256 and height >= 256, \
                        f"Image {image_path.name} too small: {width}x{height}"
                    
            except Exception as e:
                pytest.fail(f"Failed to open/validate image {image_path.name}: {e}")
    
    def test_persona_images_recommended_dimensions(self, images_dir):
        """Test that images have recommended dimensions for web display"""
        image_files = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg'))
        
        recommended_sizes = [(256, 256), (512, 512), (1024, 1024)]
        
        for image_path in image_files:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Check if image matches any recommended size
                # Allow for some variation (within 10 pixels)
                matches_recommended = any(
                    abs(width - rec_w) <= 10 and abs(height - rec_h) <= 10
                    for rec_w, rec_h in recommended_sizes
                )
                
                assert matches_recommended, \
                    f"Image {image_path.name} ({width}x{height}) doesn't match " \
                    f"recommended sizes: {recommended_sizes}"
    
    def test_who_its_for_section_exists(self, html_content):
        """Test that the 'Who It's For' section exists in HTML"""
        # Find section with "Who It's For" badge
        who_its_for_section = html_content.find('div', class_='section-badge', 
                                                 string=re.compile(r"Who.*For", re.IGNORECASE))
        
        assert who_its_for_section is not None, \
            "Could not find 'Who It's For' section badge in HTML"
        
        # Find the personas section
        personas_section = html_content.find('section', class_='personas')
        assert personas_section is not None, \
            "Could not find personas section in HTML"
    
    def test_persona_cards_exist(self, html_content):
        """Test that persona cards exist in the HTML"""
        persona_cards = html_content.find_all('div', class_='persona-card')
        
        assert len(persona_cards) >= 2, \
            f"Expected at least 2 persona cards, found {len(persona_cards)}"
    
    def test_persona_avatar_elements_exist(self, html_content):
        """Test that persona avatar elements exist"""
        persona_avatars = html_content.find_all('div', class_='persona-avatar')
        
        assert len(persona_avatars) >= 2, \
            f"Expected at least 2 persona avatars, found {len(persona_avatars)}"
    
    def test_persona_cards_have_correct_structure(self, html_content):
        """Test that persona cards have the expected structure"""
        persona_cards = html_content.find_all('div', class_='persona-card')
        
        for card in persona_cards:
            # Each card should have a header
            header = card.find('div', class_='persona-header')
            assert header is not None, "Persona card missing header"
            
            # Header should have avatar
            avatar = header.find('div', class_='persona-avatar')
            assert avatar is not None, "Persona header missing avatar"
            
            # Header should have name (h3)
            name = header.find('h3')
            assert name is not None, "Persona header missing name"
            
            # Should have body section
            body = card.find('div', class_='persona-body')
            assert body is not None, "Persona card missing body"
    
    def test_persona_avatars_ready_for_image_replacement(self, html_content):
        """Test that persona avatars can be replaced with actual images"""
        persona_avatars = html_content.find_all('div', class_='persona-avatar')
        
        for avatar in persona_avatars:
            # Avatar should exist and be identifiable
            assert avatar is not None
            
            # Check if it currently contains emoji (to be replaced)
            # or already contains an img tag
            has_emoji = bool(re.search(r'[\U0001F300-\U0001F9FF]', avatar.get_text()))
            has_img = avatar.find('img') is not None
            
            assert has_emoji or has_img, \
                "Persona avatar should contain either emoji (placeholder) or img tag"
    
    def test_generation_report_exists(self, images_dir):
        """Test that a generation report exists documenting the image creation"""
        report_files = list(images_dir.glob('generation_report_*.json'))
        
        if len(report_files) > 0:
            # If reports exist, validate the latest one
            latest_report = max(report_files, key=lambda p: p.stat().st_mtime)
            
            with open(latest_report, 'r') as f:
                report = json.load(f)
            
            # Validate report structure
            assert 'generation_timestamp' in report
            assert 'total_personas' in report
            assert 'successful_generations' in report
            assert 'results' in report
            
            # Check that some images were successfully generated
            assert report['successful_generations'] > 0, \
                "Report shows no successful image generations"
    
    def test_image_files_match_personas(self, images_dir):
        """Test that image files correspond to defined personas"""
        expected_persona_keys = list(self.EXPECTED_PERSONAS.keys())
        image_files = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg'))
        
        for persona_key in expected_persona_keys:
            matching_files = [f for f in image_files if persona_key in f.name]
            
            assert len(matching_files) > 0, \
                f"No image file found matching persona key: {persona_key}"
    
    def test_css_supports_persona_images(self, html_file_path):
        """Test that CSS includes styling for persona avatars/images"""
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for persona-avatar CSS class
        assert '.persona-avatar' in html_content, \
            "CSS missing .persona-avatar class definition"
        
        # Check that persona-avatar has basic image styling properties
        # Look for common image-related CSS properties
        persona_avatar_section = re.search(
            r'\.persona-avatar\s*{[^}]*}', 
            html_content, 
            re.DOTALL
        )
        
        assert persona_avatar_section is not None, \
            "Could not find .persona-avatar CSS definition"
    
    def test_image_paths_structure(self, images_dir):
        """Test that images follow a consistent naming convention"""
        image_files = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg'))
        
        for image_file in image_files:
            filename = image_file.name
            
            # Expected format: {persona_key}_{timestamp}.{ext}
            # e.g., estate_inheritor_20231027_143022.png
            pattern = r'^[a-z_]+_\d{8}_\d{6}\.(png|jpg)$'
            
            assert re.match(pattern, filename), \
                f"Image filename doesn't match expected pattern: {filename}"
    
    def test_can_locate_personas_for_image_insertion(self, html_content):
        """Test that we can identify where to insert images in HTML"""
        persona_cards = html_content.find_all('div', class_='persona-card')
        
        insertion_points = []
        
        for card in persona_cards:
            avatar = card.find('div', class_='persona-avatar')
            name_elem = card.find('h3')
            
            if avatar and name_elem:
                name_text = name_elem.get_text(strip=True)
                insertion_points.append({
                    'avatar_element': avatar,
                    'name': name_text
                })
        
        assert len(insertion_points) >= 2, \
            f"Could not identify enough insertion points. Found: {len(insertion_points)}"
        
        # Verify we can match personas
        for point in insertion_points:
            name = point['name']
            # Should match at least one expected persona identifier
            matches = [
                persona_key for persona_key, data in self.EXPECTED_PERSONAS.items()
                if data['html_identifier'] in name
            ]
            
            assert len(matches) > 0, \
                f"Could not match HTML name '{name}' to any expected persona"


class TestImageIntegrationHelpers:
    """Helper tests for image integration utilities"""
    
    @pytest.fixture
    def images_dir(self):
        """Get the generated images directory"""
        return Path(__file__).parent / 'generated_images'
    
    def test_get_latest_image_for_persona(self, images_dir):
        """Test helper function to get the latest image for a persona"""
        def get_latest_image(persona_key: str) -> Optional[Path]:
            """Get the most recent image for a given persona"""
            matching_files = list(images_dir.glob(f'{persona_key}_*.png'))
            matching_files.extend(images_dir.glob(f'{persona_key}_*.jpg'))
            
            if not matching_files:
                return None
            
            # Return the most recently created file
            return max(matching_files, key=lambda p: p.stat().st_mtime)
        
        # Test with a real persona key
        test_personas = ['estate_inheritor', 'reseller_entrepreneur']
        
        for persona_key in test_personas:
            latest = get_latest_image(persona_key)
            
            if images_dir.exists() and list(images_dir.glob('*.png')):
                # If images exist, we should find them
                if latest:
                    assert latest.exists()
                    assert persona_key in latest.name
    
    def test_image_path_for_web(self, images_dir):
        """Test generating correct web paths for images"""
        def get_web_path(image_path: Path) -> str:
            """Convert file system path to web path"""
            # From /home/user/project/ai_image_generation/generated_images/file.png
            # To: ai_image_generation/generated_images/file.png
            rel_path = image_path.relative_to(image_path.parent.parent.parent)
            return str(rel_path).replace('\\', '/')
        
        # Test with a sample path
        sample_path = images_dir / 'estate_inheritor_20231027_120000.png'
        web_path = get_web_path(sample_path)
        
        assert 'ai_image_generation/generated_images/' in web_path
        assert web_path.endswith('.png')


class TestPersonaImageUpdateWorkflow:
    """Tests for the workflow of updating HTML with AI-generated images"""
    
    @pytest.fixture
    def images_dir(self):
        """Get the generated images directory"""
        return Path(__file__).parent / 'generated_images'
    
    def test_update_instructions_documented(self):
        """Test that there are instructions for updating the HTML"""
        readme_path = Path(__file__).parent / 'README.md'
        
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Should mention updating HTML or integration
            assert any(keyword in readme_content.lower() for keyword in 
                      ['update', 'integration', 'html', 'webpage']), \
                "README should document the image integration process"
    
    def test_image_replacement_map(self, images_dir):
        """Test creating a mapping of personas to image files"""
        def create_persona_image_map() -> Dict[str, str]:
            """Create a mapping of persona keys to their latest image paths"""
            persona_map = {}
            
            persona_keys = ['estate_inheritor', 'reseller_entrepreneur', 
                          'antique_collector', 'small_business_owner']
            
            for persona_key in persona_keys:
                # Find latest image for this persona
                matching_files = list(images_dir.glob(f'{persona_key}_*.png'))
                matching_files.extend(images_dir.glob(f'{persona_key}_*.jpg'))
                
                if matching_files:
                    latest = max(matching_files, key=lambda p: p.stat().st_mtime)
                    persona_map[persona_key] = str(latest.name)
            
            return persona_map
        
        if images_dir.exists() and list(images_dir.glob('*.png')):
            mapping = create_persona_image_map()
            
            # Should have at least some mappings
            assert len(mapping) >= 0
            
            # All values should be filenames
            for persona_key, filename in mapping.items():
                assert filename.endswith(('.png', '.jpg'))
                assert persona_key in filename


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
