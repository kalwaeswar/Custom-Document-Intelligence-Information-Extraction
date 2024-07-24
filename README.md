# Custom Document Intelligence Information Extraction

This project showcases the development of a custom document intelligence application that leverages cognitive services in Microsoft Azure to extract information from various documents. The application is implemented using Python and Azure Cognitive Services and features a user-friendly web interface built with Streamlit.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The Custom Document Intelligence Information Extraction project aims to demonstrate the capabilities of Azure Cognitive Services in processing and extracting valuable information from documents. This project is particularly useful for automating document processing tasks, enhancing productivity, and reducing manual effort.

## Features
- **Document Processing**: Automatically process and analyze various types of documents, including PDFs and images.
- **Information Extraction**: Extract key information such as text, tables, and other structured data from documents.
- **User-Friendly Interface**: A web interface built with Streamlit to facilitate easy document upload and processing.
- **Scalability**: Leverage Azure's cloud infrastructure to handle large volumes of documents efficiently.

## Architecture
The architecture of the application includes the following components:
- **Azure Cognitive Services**: Utilize Azure's Form Recognizer and other cognitive services for document processing.
- **Python Backend**: Implement the core functionality using Python, including interaction with Azure services.
- **Streamlit Web Interface**: Build a simple and intuitive web interface for users to upload documents and view extracted information.

## Setup and Installation
To set up and run the project locally, follow these steps:

### Prerequisites
- Python 3.7 or higher
- An Azure account with access to Cognitive Services

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/custom-document-intelligence.git
    cd custom-document-intelligence
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Azure Cognitive Services:
    - Create a Form Recognizer resource in the Azure portal.
    - Obtain the API key and endpoint URL from the Azure portal.
    - Create a `.env` file in the project directory and add the following:
      ```
      AZURE_FORM_RECOGNIZER_ENDPOINT=<your-endpoint-url>
      AZURE_FORM_RECOGNIZER_KEY=<your-api-key>
      ```

## Usage
To start the application, run the following command:
```bash
streamlit run app.py
```
This will launch the Streamlit web interface in your browser, where you can upload documents and view the extracted information.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

### Steps to Contribute
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README file further based on your project's specific details and requirements.
