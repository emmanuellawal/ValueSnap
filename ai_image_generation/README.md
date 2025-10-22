# ValueSnap AI Image Generator

This module generates professional images of ValueSnap's target consumers using OpenAI's DALL-E API.

## Overview

The AI Image Generator creates realistic portraits of your target customer personas:
- **Estate Inheritors**: People managing inherited items and family collections
- **Reseller Entrepreneurs**: Individuals buying and selling items for profit  
- **Antique Collectors**: Mature collectors evaluating valuable items
- **Small Business Owners**: Shop owners needing quick item valuations

## Files

- `generate_ai_images.py` - Main image generation script
- `test_ai_generator_simple.py` - Test suite that validates personas and workflow
- `test_generate_ai_images.py` - Comprehensive test suite (requires compatible OpenAI version)
- `test_openai_client.py` - Simple OpenAI client test
- `setup_ai_images.sh` - Setup script for dependencies and environment
- `.env.example` - Environment variable template

## Quick Start

1. **Set up environment:**
   ```bash
   cd ai_image_generation
   ./setup_ai_images.sh
   ```

2. **Add your OpenAI API key:**
   ```bash
   cp .env.example ../.env
   # Edit ../.env and add your real OpenAI API key
   ```

3. **Run tests:**
   ```bash
   python test_ai_generator_simple.py
   ```

4. **Generate images:**
   ```bash
   python generate_ai_images.py
   ```

## API Key Setup

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key to your `.env` file in the root directory:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## Generated Output

Images are saved to `generated_images/` directory with:
- Professional portraits of each persona
- 1024x1024 resolution (configurable)
- PNG format
- Timestamped filenames
- JSON report with generation details

## Cost Estimation

DALL-E 3 pricing (as of 2023):
- Standard quality (1024×1024): ~$0.040 per image
- 4 personas = ~$0.16 total per generation run

## Usage in Landing Page

Generated images can be used to:
- Replace generic testimonial photos
- Add realistic user personas to marketing materials
- Create authentic-looking customer stories
- Enhance visual appeal and trustworthiness

## Troubleshooting

If you encounter OpenAI/httpx compatibility issues:
1. Run the simple test suite: `python test_ai_generator_simple.py`
2. Update dependencies: `pip install -r ../requirements.txt --upgrade`
3. Check API key format: Must start with `sk-`

## Integration

To use generated images in your landing page:
1. Generate images with this module
2. Copy desired images to your web assets directory
3. Update `index.html` to reference the new images
4. Replace placeholder testimonial photos with AI-generated personas