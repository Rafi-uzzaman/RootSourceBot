# RootSource AI 🌱

A multilingual AI-powered farming assistant that helps answer agriculture-related questions in any language using advanced AI tools and search capabilities.

## Features

- 🌍 **Multilingual Support**: Ask questions in any language and get responses in your native language
- 🔍 **Intelligent Search**: Uses Wikipedia, ArXiv, and DuckDuckGo for comprehensive farming information
- 🤖 **AI-Powered**: Leverages advanced language models for accurate responses
- 💬 **Interactive Chat**: Streamlit-based user-friendly interface
- 🧠 **Memory**: Maintains conversation context for better interactions

## Technologies Used

- **Streamlit** - Web interface
- **LangChain** - AI agent framework
- **OpenAI/Groq** - Language model integration
- **Wikipedia/ArXiv/DuckDuckGo** - Information sources
- **Google Translator** - Multilingual support

## Setup and Installation

### Prerequisites
- Python 3.11+
- GROQ API key

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rafi-uzzaman/RootSourceBot.git
   cd RootSourceBot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Deployment

### Streamlit Community Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `GROQ_API_KEY` in the secrets section
5. Deploy!

### Other Deployment Options

- **Railway**: Connect GitHub repo and deploy
- **Render**: Deploy from GitHub with automatic builds
- **Heroku**: Use the provided Procfile for deployment

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for AI model access | Yes |

## Usage

1. Open the application in your browser
2. Type your farming-related question in any language
3. The AI will detect your language and provide a response
4. Continue the conversation for follow-up questions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support, please open an issue on GitHub or contact the maintainers.
RootSource AI, Ask your farming-related questions in any language, and get accurate answers!
