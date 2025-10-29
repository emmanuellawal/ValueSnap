"""
Utility script to update index.html with AI-generated persona images

This script:
1. Finds the latest AI-generated images for each persona
2. Updates the HTML to replace emoji avatars with actual images
3. Creates a backup of the original HTML
4. Validates the updates
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from bs4 import BeautifulSoup


class PersonaImageUpdater:
    """Updates HTML with AI-generated persona images"""
    
    # Mapping of persona keys to their HTML identifiers
    PERSONA_MAPPING = {
        'estate_inheritor': {
            'html_name': 'Emeka',
            'description': 'Estate Manager'
        },
        'reseller_entrepreneur': {
            'html_name': 'Jake',
            'description': 'Reseller'
        }
    }
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the updater"""
        if project_root is None:
            # Assume script is in ai_image_generation directory
            project_root = Path(__file__).parent.parent
        
        self.project_root = Path(project_root)
        self.html_path = self.project_root / 'index.html'
        self.images_dir = Path(__file__).parent / 'generated_images'
        
    def get_latest_image(self, persona_key: str) -> Optional[Path]:
        """Get the most recent image for a given persona"""
        matching_files = list(self.images_dir.glob(f'{persona_key}_*.png'))
        matching_files.extend(self.images_dir.glob(f'{persona_key}_*.jpg'))
        
        if not matching_files:
            return None
        
        # Return the most recently created file
        return max(matching_files, key=lambda p: p.stat().st_mtime)
    
    def create_backup(self) -> Path:
        """Create a backup of the original HTML file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.html_path.with_suffix(f'.backup_{timestamp}.html')
        
        shutil.copy2(self.html_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        
        return backup_path
    
    def get_web_image_path(self, image_path: Path) -> str:
        """Convert file system path to web-relative path"""
        # Get path relative to project root
        try:
            rel_path = image_path.relative_to(self.project_root)
            return str(rel_path).replace('\\', '/')
        except ValueError:
            # If image is not under project root, use relative to HTML
            rel_path = image_path.relative_to(self.html_path.parent)
            return str(rel_path).replace('\\', '/')
    
    def create_image_tag(self, image_path: Path, alt_text: str) -> str:
        """Create an HTML img tag for the persona image"""
        web_path = self.get_web_image_path(image_path)
        
        img_tag = f'<img src="{web_path}" alt="{alt_text}" class="persona-image" />'
        return img_tag
    
    def update_html_with_images(self, dry_run: bool = False) -> Dict:
        """
        Update the HTML file with AI-generated images
        
        Args:
            dry_run: If True, only show what would be changed without actually modifying
        
        Returns:
            Dict with update results
        """
        results = {
            'updated_personas': [],
            'missing_images': [],
            'errors': []
        }
        
        # Read HTML file
        if not self.html_path.exists():
            results['errors'].append(f"HTML file not found: {self.html_path}")
            return results
        
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all persona cards
        persona_cards = soup.find_all('div', class_='persona-card')
        
        for card in persona_cards:
            # Find the name in this card
            name_elem = card.find('h3')
            if not name_elem:
                continue
            
            name_text = name_elem.get_text(strip=True)
            
            # Match to a persona
            persona_key = None
            persona_info = None
            
            for key, info in self.PERSONA_MAPPING.items():
                if info['html_name'] in name_text:
                    persona_key = key
                    persona_info = info
                    break
            
            if not persona_key:
                continue
            
            # Get the image for this persona
            image_path = self.get_latest_image(persona_key)
            
            if not image_path:
                results['missing_images'].append(persona_key)
                print(f"⚠️  No image found for persona: {persona_key}")
                continue
            
            # Find the avatar element
            avatar = card.find('div', class_='persona-avatar')
            
            if not avatar:
                results['errors'].append(f"No avatar element found for {persona_key}")
                continue
            
            # Create the new image tag
            alt_text = f"{persona_info['html_name']} - {persona_info['description']}"
            img_tag = self.create_image_tag(image_path, alt_text)
            
            if dry_run:
                print(f"\n🔍 Would update {persona_key}:")
                print(f"   Current: {avatar}")
                print(f"   New: {img_tag}")
            else:
                # Replace the content of the avatar div
                avatar.clear()
                new_img = soup.new_tag('img', 
                                       src=self.get_web_image_path(image_path),
                                       alt=alt_text,
                                       attrs={'class': 'persona-image'})
                avatar.append(new_img)
                
                results['updated_personas'].append({
                    'persona_key': persona_key,
                    'name': persona_info['html_name'],
                    'image_path': str(image_path.name)
                })
                
                print(f"✅ Updated {persona_key} with image: {image_path.name}")
        
        # Write updated HTML if not dry run
        if not dry_run and results['updated_personas']:
            # Create backup first
            backup_path = self.create_backup()
            
            # Write updated HTML
            with open(self.html_path, 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            
            print(f"\n✅ HTML updated successfully!")
            print(f"   Backup saved to: {backup_path.name}")
            print(f"   Updated {len(results['updated_personas'])} persona(s)")
        
        return results
    
    def add_persona_image_css(self, dry_run: bool = False) -> bool:
        """Add CSS styling for persona images if not already present"""
        if not self.html_path.exists():
            return False
        
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if persona-image CSS already exists
        if '.persona-image' in html_content:
            print("ℹ️  CSS for .persona-image already exists")
            return True
        
        # CSS to add
        persona_image_css = """
        .persona-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
        }
        """
        
        # Find where to insert (after .persona-avatar style)
        pattern = r'(\.persona-avatar\s*{[^}]*})'
        
        match = re.search(pattern, html_content, re.DOTALL)
        
        if match:
            insert_position = match.end()
            
            if dry_run:
                print(f"🔍 Would add persona-image CSS after .persona-avatar")
                print(f"   CSS to add: {persona_image_css.strip()}")
                return True
            else:
                updated_content = (
                    html_content[:insert_position] + 
                    persona_image_css + 
                    html_content[insert_position:]
                )
                
                with open(self.html_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print("✅ Added .persona-image CSS styling")
                return True
        else:
            print("⚠️  Could not find .persona-avatar CSS to insert after")
            return False
    
    def validate_updates(self) -> Dict:
        """Validate that images are properly integrated in HTML"""
        validation = {
            'valid': True,
            'issues': [],
            'images_found': []
        }
        
        if not self.html_path.exists():
            validation['valid'] = False
            validation['issues'].append("HTML file not found")
            return validation
        
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all persona avatar elements
        persona_avatars = soup.find_all('div', class_='persona-avatar')
        
        for avatar in persona_avatars:
            img = avatar.find('img')
            
            if img:
                src = img.get('src', '')
                alt = img.get('alt', '')
                
                validation['images_found'].append({
                    'src': src,
                    'alt': alt
                })
                
                # Validate image path
                image_path = self.project_root / src
                if not image_path.exists():
                    validation['valid'] = False
                    validation['issues'].append(f"Image file not found: {src}")
                
                # Validate alt text
                if not alt:
                    validation['issues'].append(f"Missing alt text for image: {src}")
        
        if not validation['images_found']:
            validation['valid'] = False
            validation['issues'].append("No persona images found in HTML")
        
        return validation


def main():
    """Main function to update HTML with persona images"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Update index.html with AI-generated persona images'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without actually modifying files'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate existing image integration'
    )
    parser.add_argument(
        '--add-css',
        action='store_true',
        help='Add CSS styling for persona images'
    )
    
    args = parser.parse_args()
    
    updater = PersonaImageUpdater()
    
    print("🎨 ValueSnap Persona Image Updater")
    print("=" * 50)
    
    if args.validate:
        print("\n📋 Validating current integration...")
        validation = updater.validate_updates()
        
        if validation['valid']:
            print("✅ Validation passed!")
            print(f"   Found {len(validation['images_found'])} persona image(s)")
        else:
            print("❌ Validation failed!")
            for issue in validation['issues']:
                print(f"   • {issue}")
        
        return 0 if validation['valid'] else 1
    
    if args.add_css:
        print("\n🎨 Adding CSS for persona images...")
        updater.add_persona_image_css(dry_run=args.dry_run)
    
    # Update HTML with images
    print(f"\n{'🔍 DRY RUN - ' if args.dry_run else ''}Updating HTML with persona images...")
    results = updater.update_html_with_images(dry_run=args.dry_run)
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   ✅ Updated: {len(results['updated_personas'])}")
    print(f"   ⚠️  Missing images: {len(results['missing_images'])}")
    print(f"   ❌ Errors: {len(results['errors'])}")
    
    if results['missing_images']:
        print(f"\n   Missing images for: {', '.join(results['missing_images'])}")
    
    if results['errors']:
        print(f"\n   Errors:")
        for error in results['errors']:
            print(f"      • {error}")
    
    if not args.dry_run and results['updated_personas']:
        print(f"\n✨ Next steps:")
        print(f"   1. Review the updated index.html file")
        print(f"   2. Test the page in a browser")
        print(f"   3. Adjust CSS if needed for optimal display")
    
    return 0


if __name__ == '__main__':
    exit(main())
