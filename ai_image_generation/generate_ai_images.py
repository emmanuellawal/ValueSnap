"""
ValueSnap AI Image Generator
Generates professional images of target consumers using OpenAI's DALL-E API
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import openai
import requests
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ValueSnapImageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the image generator with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Create directories for generated images
        self.images_dir = Path('generated_images')
        self.images_dir.mkdir(exist_ok=True)
        
        # Consumer personas based on ValueSnap's target audience
        self.consumer_personas = {
            "estate_inheritor": {
                "name": "Estate Inheritor",
                "age_range": "35-55",
                "description": "Professional woman who inherited family antiques and collectibles",
                "prompt": "Professional portrait of a 45-year-old woman in business attire, standing in a home office with vintage furniture and inherited antiques in the background, warm lighting, confident expression, realistic photography style"
            },
            "reseller_entrepreneur": {
                "name": "Reseller Entrepreneur", 
                "age_range": "25-40",
                "description": "Young professional who buys and sells items for profit",
                "prompt": "Portrait of a 32-year-old person in casual business attire, sitting at a desk with multiple items for resale (vintage items, electronics, collectibles) organized around them, modern apartment setting, entrepreneurial vibe, realistic photography style"
            },
            "antique_collector": {
                "name": "Antique Collector",
                "age_range": "50-70", 
                "description": "Mature collector evaluating valuable items",
                "prompt": "Distinguished 60-year-old person examining an antique item with a magnifying glass, surrounded by carefully curated vintage items and books, library or study setting, sophisticated atmosphere, realistic photography style"
            },
            "small_business_owner": {
                "name": "Small Business Owner",
                "age_range": "30-50",
                "description": "Shop owner who needs quick item valuations",
                "prompt": "Portrait of a 40-year-old small business owner in their vintage/consignment shop, surrounded by diverse items for sale, friendly and approachable expression, natural lighting, realistic photography style"
            }
        }
    
    def generate_consumer_image(self, persona_key: str, size: str = "512x512") -> Dict:
        """
        Generate an image for a specific consumer persona
        
        Args:
            persona_key: Key for the consumer persona
            size: Image size (256x256, 512x512, 1024x1024)
            
        Returns:
            Dict with image info and file path
        """
        if persona_key not in self.consumer_personas:
            raise ValueError(f"Unknown persona: {persona_key}. Available: {list(self.consumer_personas.keys())}")
        
        persona = self.consumer_personas[persona_key]
        
        try:
            print(f"Generating image for {persona['name']}...")
            
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=persona['prompt'],
                size=size,
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download and save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{persona_key}_{timestamp}.png"
            file_path = self.images_dir / filename
            
            # Download image
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(img_response.content)
            
            # Verify image was saved correctly
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    format = img.format
            except Exception as e:
                raise Exception(f"Failed to verify saved image: {e}")
            
            result = {
                'persona_key': persona_key,
                'persona_name': persona['name'],
                'image_url': image_url,
                'file_path': str(file_path),
                'filename': filename,
                'size': f"{width}x{height}",
                'format': format,
                'timestamp': timestamp,
                'prompt_used': persona['prompt']
            }
            
            print(f"✅ Successfully generated {persona['name']} image: {filename}")
            return result
            
        except Exception as e:
            error_msg = f"Failed to generate image for {persona['name']}: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def generate_all_personas(self, size: str = "512x512", delay: int = 2) -> List[Dict]:
        """
        Generate images for all consumer personas
        
        Args:
            size: Image size for all images
            delay: Delay between API calls (seconds)
            
        Returns:
            List of image generation results
        """
        results = []
        
        for i, persona_key in enumerate(self.consumer_personas.keys()):
            try:
                result = self.generate_consumer_image(persona_key, size)
                results.append(result)
                
                # Add delay between requests to respect rate limits
                if i < len(self.consumer_personas) - 1:
                    print(f"Waiting {delay} seconds before next generation...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"Failed to generate {persona_key}: {e}")
                results.append({
                    'persona_key': persona_key,
                    'error': str(e),
                    'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
                })
        
        return results
    
    def save_generation_report(self, results: List[Dict], filename: str = None) -> str:
        """Save generation results to a JSON report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generation_report_{timestamp}.json"
        
        report_path = self.images_dir / filename
        
        report = {
            'generation_timestamp': datetime.now().isoformat(),
            'total_personas': len(self.consumer_personas),
            'successful_generations': len([r for r in results if 'error' not in r]),
            'failed_generations': len([r for r in results if 'error' in r]),
            'results': results
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Generation report saved: {report_path}")
        return str(report_path)
    
    def get_persona_info(self) -> Dict:
        """Get information about all available personas"""
        return {
            key: {
                'name': persona['name'],
                'age_range': persona['age_range'], 
                'description': persona['description']
            }
            for key, persona in self.consumer_personas.items()
        }


def main():
    """Main function to generate all consumer persona images"""
    try:
        generator = ValueSnapImageGenerator()
        
        print("🎨 ValueSnap Consumer Image Generator")
        print("=" * 50)
        
        # Show available personas
        personas = generator.get_persona_info()
        print("\nTarget Consumer Personas:")
        for key, info in personas.items():
            print(f"  • {info['name']} ({info['age_range']}): {info['description']}")
        
        print(f"\n🚀 Generating images for {len(personas)} personas...")
        
        # Generate all images
        results = generator.generate_all_personas()
        
        # Save report
        report_path = generator.save_generation_report(results)
        
        # Print summary
        successful = len([r for r in results if 'error' not in r])
        failed = len([r for r in results if 'error' in r])
        
        print(f"\n📈 Generation Summary:")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📊 Report: {report_path}")
        
        if successful > 0:
            print(f"\n🖼️  Generated images saved in: {generator.images_dir}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
