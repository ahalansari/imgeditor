# Qwen Image Editor Flask Application

A Flask web application that integrates with the Qwen-Image-Edit model from Hugging Face to perform AI-powered image editing with text prompts.

## ✨ Features

- 📷 Upload images (PNG, JPG, JPEG, GIF) 
- 🤖 AI-powered image editing with natural language prompts
- 🎨 Support for semantic editing, appearance editing, and object manipulation
- 💻 Optimized for Mac M4 Max with MPS acceleration
- 🖼️ Side-by-side comparison of original and edited images
- 📥 Download processed images
- 💡 Built-in prompt examples and suggestions

## 🚀 Quick Start

### Prerequisites
- **Mac M4 Max** (optimized for Apple Silicon)
- **Python 3.8+** 
- **16GB+ RAM** (for model loading)
- **~20GB free disk space** (for model weights)

### Installation

1. **Clone and setup:**
```bash
git clone <repository-url>
cd imgeditor
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python run.py
# OR
python app.py
```

4. **Open your browser:**
```
http://localhost:5001
```

## 📖 Usage

1. **Upload an image** using the drag-and-drop interface
2. **Enter editing instructions** in natural language:
   - *Semantic editing*: "Change style to Studio Ghibli animation"
   - *Appearance editing*: "Change the background to a forest"
   - *Object manipulation*: "Add sunglasses to the person"
   - *Text editing*: "Change the sign text to 'Hello World'"
3. **Click "Upload and Process"** and wait for AI processing
4. **View results** with side-by-side comparison
5. **Download** the edited image

## 🛠️ Technical Details

### Architecture
- **Flask 2.3.3** web server with modern responsive UI
- **Qwen-Image-Edit** pipeline with optimized parameters
- **MPS acceleration** for Apple Silicon
- **Memory optimizations** with attention slicing
- **Secure file handling** with UUID-based naming

### Model Configuration
- **Device**: MPS (Metal Performance Shaders) for Mac M4 Max
- **Precision**: bfloat16 for optimal Apple Silicon performance  
- **Parameters**: `true_cfg_scale=4.0`, `num_inference_steps=50`
- **Memory**: Attention slicing enabled for efficiency

### Performance
- **First run**: ~2-3 minutes for model download and loading
- **Subsequent runs**: ~30-60 seconds for processing per image
- **Model size**: ~20GB cached locally after first download

## 🔧 Troubleshooting

### Common Issues
- **Out of memory**: Reduce image size or enable CPU offload
- **Slow processing**: Normal on first run; subsequent runs are faster
- **Model download fails**: Check internet connection and disk space

### Debug Mode
```bash
export FLASK_ENV=development
python app.py
```

## 📁 Project Structure
```
imgeditor/
├── app.py              # Main Flask application  
├── run.py              # Optimized startup script
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── uploads/           # User uploaded images
├── output/            # AI processed images  
└── README.md          # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch  
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.