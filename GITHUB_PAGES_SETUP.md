# GitHub Pages Deployment Guide

## ✅ What's Already Configured

Your repository is ready for GitHub Pages deployment with:
- GitHub Actions workflow (`.github/workflows/deploy.yml`)
- Automated deployment on push to `main` branch
- Proper permissions and settings

## 🚀 Steps to Deploy

### 1. Commit and Push Your Changes

```bash
git add .
git commit -m "Add enhanced landing page and AI image generation"
git push origin main
```

### 2. Enable GitHub Pages in Repository Settings

1. Go to your repository: https://github.com/emmanuellawal/ValueSnap
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Build and deployment**:
   - Source: Select **GitHub Actions**
5. Save the settings

### 3. Wait for Deployment

- The GitHub Actions workflow will automatically run
- Check progress at: https://github.com/emmanuellawal/ValueSnap/actions
- First deployment takes ~1-2 minutes

### 4. Access Your Site

Your site will be available at:
**https://emmanuellawal.github.io/ValueSnap/**

## 🔄 Automatic Updates

Every time you push to the `main` branch:
- GitHub Actions automatically rebuilds your site
- Changes appear live within 1-2 minutes
- No manual intervention needed

## 📝 What Gets Deployed

The workflow deploys:
- `index.html` - Your enhanced landing page
- `favicon.svg`, `favicon.ico`, `favicon-32x32.png` - Site icons
- Any markdown files (like README.md)

## 🎨 Custom Domain (Optional)

To use a custom domain like `valuesnap.com`:

1. Create a `CNAME` file in your repository root:
   ```
   valuesnap.com
   ```

2. Add DNS records at your domain provider:
   - Type: CNAME
   - Name: www
   - Value: emmanuellawal.github.io

3. In GitHub Pages settings, enter your custom domain

## 🐛 Troubleshooting

### Deployment Failed?
- Check Actions tab for error messages
- Verify GitHub Pages is enabled in Settings
- Ensure workflow has proper permissions

### Site Not Updating?
- Clear browser cache (Ctrl+Shift+R)
- Check if commit triggered workflow
- Wait 2-3 minutes for propagation

### 404 Error?
- Verify source is set to "GitHub Actions"
- Check that index.html is in repository root
- Ensure workflow completed successfully

## 📊 Monitoring

- View deployment history: Settings → Pages
- Check workflow runs: Actions tab
- See build logs: Click on any workflow run

## 🎯 Next Steps After Deployment

1. ✅ Verify site loads at the GitHub Pages URL
2. 🖼️ Generate AI images (see `ai_image_generation/README.md`)
3. 🎨 Integrate generated images into landing page
4. 🚀 Share your live site!

---

**Quick Deploy Command:**
```bash
git add . && git commit -m "Deploy to GitHub Pages" && git push origin main
```
