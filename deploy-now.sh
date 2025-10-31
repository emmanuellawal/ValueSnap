#!/bin/bash

# Quick deployment script - run this after making the fixes
cd /home/elawa/projects/ValueSnap

echo "🚀 Deploying fixes to GitHub Pages..."

git add index.html deploy-gh-pages.sh GITHUB_PAGES_FIX.md
git commit -m "Fix GitHub Pages deployment - update asset paths to relative"
git push origin main

echo ""
echo "✅ Changes pushed to GitHub!"
echo "🌐 Your site will update at: https://emmanuellawal.github.io/ValueSnap/"
echo "⏱️  Wait 1-2 minutes for GitHub Pages to rebuild"
echo ""
echo "💡 Tip: Press Ctrl+Shift+R in your browser to hard refresh and see changes"
