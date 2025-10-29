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
- 512x512 resolution (default, configurable)
- PNG format
- Timestamped filenames
- JSON report with generation details

## Cost Estimation

DALL-E 2 pricing (as of 2025):
- 512×512 resolution: ~$0.018 per image
- 4 personas = ~$0.072 total per generation run

**Cost savings:** Using DALL-E 2 instead of DALL-E 3 saves ~55% ($0.072 vs $0.160)

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
1. Generate images with this module: `python generate_ai_images.py`
2. Run the integration tests: `pytest test_persona_image_integration.py -v`
3. Update HTML with images: `python update_persona_images.py --dry-run` (preview changes)
4. Apply updates: `python update_persona_images.py` (updates index.html)
5. Validate integration: `python update_persona_images.py --validate`

## Testing

### Test Suites Available

1. **test_persona_image_integration.py** - Comprehensive tests for image integration
   - Verifies images exist in correct locations
   - Validates image formats and dimensions
   - Checks HTML structure for persona cards
   - Tests that images map correctly to personas
   - Validates web paths and CSS support

2. **test_generate_ai_images.py** - Tests for image generation functionality
   - Validates API integration
   - Tests persona definitions
   - Checks generation workflow

3. **test_ai_generator_simple.py** - Simple validation tests
   - Basic persona structure tests
   - Lightweight validation

### Running Tests

Run all integration tests:
```bash
pytest test_persona_image_integration.py -v
```

Run specific test classes:
```bash
# Test image integration only
pytest test_persona_image_integration.py::TestPersonaImageIntegration -v

# Test helper functions
pytest test_persona_image_integration.py::TestImageIntegrationHelpers -v

# Test update workflow
pytest test_persona_image_integration.py::TestPersonaImageUpdateWorkflow -v
```

Run with detailed output:
```bash
pytest test_persona_image_integration.py -v -s
```

### What the Tests Verify

✅ **Image Generation**
- Images exist for all personas
- Valid PNG/JPEG format
- Correct dimensions (256x256 minimum, preferably 512x512 or 1024x1024)
- Proper naming convention (persona_key_timestamp.ext)

✅ **HTML Structure**
- "Who It's For" section exists
- Persona cards have correct structure
- Avatar elements are present and accessible
- CSS classes are properly defined

✅ **Integration Points**
- Can locate where to insert images
- Persona names match between generator and HTML
- Image paths are web-compatible
- Generation reports exist and are valid

✅ **Image Placement**
- Images are in ai_image_generation/generated_images/
- Web paths are correctly formatted
- Images can be referenced from index.html

### Expected Test Results

When tests pass, you'll see output like:
```
test_persona_image_integration.py::TestPersonaImageIntegration::test_images_directory_exists PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_images_generated PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_images_valid_format PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_who_its_for_section_exists PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_cards_exist PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_avatar_elements_exist PASSED
```

### Troubleshooting Test Failures

**No images found**: Run `python generate_ai_images.py` first to generate images

**HTML section not found**: Verify index.html has the "Who It's For" section with class="personas"

**Invalid image format**: Regenerate images with correct settings

**Path issues**: Ensure tests are run from the ai_image_generation directory