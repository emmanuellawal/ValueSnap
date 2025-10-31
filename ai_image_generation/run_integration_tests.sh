#!/bin/bash
# Run all persona image integration tests

echo "🧪 ValueSnap Persona Image Integration Tests"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "test_persona_image_integration.py" ]; then
    echo "❌ Error: Must be run from the ai_image_generation directory"
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ Error: pytest not installed"
    echo "Install with: pip install -r requirements.txt"
    exit 1
fi

# Check if images exist
if [ ! -d "generated_images" ] || [ -z "$(ls -A generated_images/*.png 2>/dev/null)" ]; then
    echo "⚠️  Warning: No images found in generated_images/"
    echo "   Generate images first with: python generate_ai_images.py"
    echo ""
fi

# Run the tests
echo "Running integration tests..."
echo ""

pytest test_persona_image_integration.py -v --tb=short

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed. See output above for details."
fi

exit $exit_code
