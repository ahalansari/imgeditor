#!/bin/bash

echo "🚀 GitHub Setup Script for Qwen Image Editor"
echo "=============================================="

# Check if user provided GitHub username
if [ -z "$1" ]; then
    echo "❌ Please provide your GitHub username"
    echo "Usage: ./setup_github.sh YOUR_GITHUB_USERNAME"
    echo "Example: ./setup_github.sh ahmad"
    exit 1
fi

USERNAME=$1
REPO_NAME="qwen-image-editor"

echo "📝 Setting up GitHub repository..."
echo "Username: $USERNAME"
echo "Repository: $REPO_NAME"
echo ""

# Add remote
echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git

# Check if remote was added successfully
if git remote -v | grep -q origin; then
    echo "✅ Remote added successfully"
else
    echo "❌ Failed to add remote"
    exit 1
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Repository pushed to GitHub"
    echo "🌐 View at: https://github.com/$USERNAME/$REPO_NAME"
    echo ""
    echo "📋 Next steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Add topics/tags: ai, image-editing, qwen, flask, pytorch"
    echo "3. Enable GitHub Pages (optional) for documentation"
    echo "4. Add a star ⭐ to show it off!"
else
    echo "❌ Failed to push to GitHub"
    echo "Make sure you:"
    echo "1. Created the repository on GitHub"
    echo "2. Have push permissions"
    echo "3. Are authenticated with GitHub"
fi
