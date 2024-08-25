# Build System Visualization

## Overview

This project is a full-stack application designed to visualize a build system as a Directed Acyclic Graph (DAG). The application includes features for node search, graph visualization, and detailed node information display. It uses Alpine.js and HTMX for interactivity, Flask for backend services, and Tailwind CSS for styling.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.6+**: Download from [python.org](https://www.python.org/downloads/).
- **pip3**: Included with Python. Verify installation by running:

  ```bash
  pip3 --version
  ```

## Getting Started

To set up the project on your local machine, follow these steps:

1. **Clone the Repository**: Clone the project repository to your local machine.

   ```bash
   git clone https://github.com/kjmj/Zipline-Take-Home.git
   cd Zipline-Take-Home
   ```

2. **Create a Virtual Environment**: In your project directory, create a virtual environment.

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**: Activate it as follows:

   - **On Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**: With the virtual environment activated, install the required dependencies.

   ```bash
   pip3 install -r requirements.txt
   ```

5. **Graph Data**: The `graphs` folder contains JSON files representing various graphs. These files will be read by the Flask server and used to generate the visualizations on the frontend. The default graph file is `graph1.json`, but you can specify other graph files by changing the `GRAPH_FILENAME` variable in `app.py`.

6. **Run the Application**: Start the Flask server to run the application.

   ```bash
   python3 app.py
   ```

7. **Open in Browser**: Navigate to `http://127.0.0.1:5000` in your browser to view the application.

## Testing Different Graphs

You can test different graph files by placing them in the `graphs` folder and updating the `GRAPH_FILENAME` variable in `app.py` to the desired file name (excluding the `.json` extension). For example, to use `graph2.json`, set:

```python
GRAPH_FILENAME = 'graph2'
```

## Notes

- Ensure the virtual environment is activated when working on this project.
- If you encounter issues, verify that all dependencies are installed and the Flask server is correctly serving the graph data.
