# Persona Image Integration Workflow

This guide walks you through generating AI images and integrating them into the "Who It's For" section of your ValueSnap landing page.

## Overview

The persona image integration system:
1. ✅ Generates professional AI images of your target consumers
2. ✅ Tests that images are in the correct locations
3. ✅ Validates HTML structure for image placement
4. ✅ Provides utilities to update the webpage automatically
5. ✅ Ensures all integration points are working correctly

## Step-by-Step Workflow

### Step 1: Generate AI Images

```bash
cd ai_image_generation
python generate_ai_images.py
```

This will create:
- `generated_images/estate_inheritor_[timestamp].png`
- `generated_images/reseller_entrepreneur_[timestamp].png`
- `generated_images/antique_collector_[timestamp].png`
- `generated_images/small_business_owner_[timestamp].png`
- `generated_images/generation_report_[timestamp].json`

**Expected Output:**
```
🎨 ValueSnap Consumer Image Generator
==================================================

Target Consumer Personas:
  • Estate Inheritor (35-55): Professional woman who inherited family antiques...
  • Reseller Entrepreneur (25-40): Young professional who buys and sells items...
  
🚀 Generating images for 4 personas...
Generating image for Estate Inheritor...
✅ Successfully generated Estate Inheritor image: estate_inheritor_20231027_143022.png
...
```

### Step 2: Run Integration Tests

```bash
# Run all tests
pytest test_persona_image_integration.py -v

# Or use the convenience script
./run_integration_tests.sh
```

**What Gets Tested:**

✅ Images directory exists  
✅ Images generated for all personas  
✅ Images are valid PNG/JPEG format  
✅ Images have correct dimensions (≥256x256)  
✅ "Who It's For" section exists in HTML  
✅ Persona cards have correct structure  
✅ Avatar elements ready for image replacement  
✅ CSS supports persona images  
✅ Image filenames follow naming convention  
✅ Can locate insertion points in HTML  

**Expected Test Output:**
```
test_persona_image_integration.py::TestPersonaImageIntegration::test_images_directory_exists PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_images_generated PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_images_valid_format PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_images_recommended_dimensions PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_who_its_for_section_exists PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_cards_exist PASSED
test_persona_image_integration.py::TestPersonaImageIntegration::test_persona_avatar_elements_exist PASSED
...

✅ All tests passed!
```

### Step 3: Preview HTML Updates (Dry Run)

```bash
python update_persona_images.py --dry-run
```

This shows what will be changed without modifying any files.

**Expected Output:**
```
🎨 ValueSnap Persona Image Updater
==================================================

🔍 DRY RUN - Updating HTML with persona images...

🔍 Would update estate_inheritor:
   Current: <div class="persona-avatar">👩‍💼</div>
   New: <img src="ai_image_generation/generated_images/estate_inheritor_20231027_143022.png" 
            alt="Emeka - Estate Manager" class="persona-image" />

🔍 Would update reseller_entrepreneur:
   Current: <div class="persona-avatar">👨‍💻</div>
   New: <img src="ai_image_generation/generated_images/reseller_entrepreneur_20231027_143122.png" 
            alt="Jake - Reseller" class="persona-image" />

📊 Summary:
   ✅ Updated: 2
   ⚠️  Missing images: 0
   ❌ Errors: 0
```

### Step 4: Add CSS Styling (Optional)

If `.persona-image` CSS doesn't exist yet:

```bash
python update_persona_images.py --add-css
```

This adds styling to make images display correctly in circular avatars.

### Step 5: Apply the Updates

```bash
python update_persona_images.py
```

This will:
1. ✅ Create a backup of `index.html` (e.g., `index.backup_20231027_143522.html`)
2. ✅ Replace emoji avatars with actual AI-generated images
3. ✅ Update image paths to be web-compatible
4. ✅ Add alt text for accessibility

**Expected Output:**
```
🎨 ValueSnap Persona Image Updater
==================================================

Updating HTML with persona images...
✅ Updated estate_inheritor with image: estate_inheritor_20231027_143022.png
✅ Updated reseller_entrepreneur with image: reseller_entrepreneur_20231027_143122.png
✅ Backup created: index.backup_20231027_143522.html

✅ HTML updated successfully!
   Backup saved to: index.backup_20231027_143522.html
   Updated 2 persona(s)

✨ Next steps:
   1. Review the updated index.html file
   2. Test the page in a browser
   3. Adjust CSS if needed for optimal display
```

### Step 6: Validate Integration

```bash
python update_persona_images.py --validate
```

Verifies that images are properly integrated.

**Expected Output:**
```
📋 Validating current integration...
✅ Validation passed!
   Found 2 persona image(s)
```

### Step 7: Test in Browser

1. Open `index.html` in a web browser
2. Scroll to the "Who It's For" section
3. Verify images display correctly
4. Check mobile responsiveness

## Troubleshooting

### No Images Generated

**Problem:** `No images found in generated_images directory`

**Solution:**
```bash
# Make sure OpenAI API key is set
echo $OPENAI_API_KEY

# Or check .env file
cat ../.env

# Generate images
python generate_ai_images.py
```

### Test Failures

**Problem:** `test_persona_images_generated FAILED`

**Solution:** Generate images first:
```bash
python generate_ai_images.py
```

---

**Problem:** `test_who_its_for_section_exists FAILED`

**Solution:** Verify `index.html` has the personas section:
```bash
grep -n "Who.*For" ../index.html
grep -n "class=\"personas\"" ../index.html
```

---

**Problem:** `test_persona_images_valid_format FAILED`

**Solution:** Regenerate images with valid format:
```bash
rm generated_images/*
python generate_ai_images.py
```

### Image Not Displaying in Browser

**Problem:** Broken image icon or 404 error

**Solution:** Check image paths:
```bash
# Verify images exist
ls -la generated_images/

# Check HTML image src attributes
grep -A 2 'persona-avatar' ../index.html

# Ensure relative paths are correct
# Should be: ai_image_generation/generated_images/[filename]
```

### CSS Issues

**Problem:** Images not circular or wrong size

**Solution:** Update CSS:
```css
.persona-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    /* ... other styles ... */
}

.persona-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
```

## File Reference

### Generated Files

- `generated_images/estate_inheritor_*.png` - Estate inheritor persona image
- `generated_images/reseller_entrepreneur_*.png` - Reseller entrepreneur persona image
- `generated_images/antique_collector_*.png` - Antique collector persona image
- `generated_images/small_business_owner_*.png` - Small business owner persona image
- `generated_images/generation_report_*.json` - Generation metadata and results
- `index.backup_*.html` - Backup of original HTML (created before updates)

### Test Files

- `test_persona_image_integration.py` - Main integration test suite
- `test_generate_ai_images.py` - Image generation tests
- `test_ai_generator_simple.py` - Simple validation tests

### Utility Scripts

- `generate_ai_images.py` - Generate AI images
- `update_persona_images.py` - Update HTML with images
- `run_integration_tests.sh` - Run all tests

## Best Practices

1. ✅ Always run tests before and after generating images
2. ✅ Use `--dry-run` before applying updates
3. ✅ Keep backups of your HTML files
4. ✅ Validate integration after updates
5. ✅ Test in multiple browsers
6. ✅ Check mobile responsiveness
7. ✅ Regenerate images if personas change

## Next Steps

After successful integration:

1. **Customize Personas**: Edit persona prompts in `generate_ai_images.py`
2. **Regenerate**: Run `python generate_ai_images.py` again
3. **Update HTML**: Run `python update_persona_images.py`
4. **Test**: Verify in browser
5. **Deploy**: Push changes to production

## Quick Commands Reference

```bash
# Generate images
python generate_ai_images.py

# Run tests
pytest test_persona_image_integration.py -v

# Preview changes
python update_persona_images.py --dry-run

# Apply updates
python update_persona_images.py

# Validate
python update_persona_images.py --validate

# Add CSS
python update_persona_images.py --add-css
```

## Support

If you encounter issues:
1. Check this workflow guide
2. Review test output for specific errors
3. Verify all dependencies are installed: `pip install -r requirements.txt`
4. Ensure OpenAI API key is valid and has credits
