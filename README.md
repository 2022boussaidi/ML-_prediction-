

# ML Prediction Platform

## Overview

This project provides a comprehensive backend solution for automating the training of machine learning models using **H2O.ai** to perform predictive tasks. The platform leverages **Flask** as the web framework, **Swagger** for API documentation and testing, and **MongoDB** to store trained models for each user. Each user has a workspace containing relevant files (datasets) and projects (where trained models are stored).

## Features

### 1. Model Training Automation
- **H2O.ai Integration**: Automate the training of machine learning models using H2O.ai.
- **Predictive Tasks**: Perform various predictive tasks with trained models.

### 2. API Development and Documentation
- **Flask Framework**: Use Flask to build and deploy the web application.
- **Swagger Integration**: Implement Swagger for API documentation and testing, making it easier for developers to understand and interact with the APIs.

### 3. Data and Model Management
- **MongoDB Storage**: Store trained models and relevant data for each user in MongoDB.
- **User Workspaces**: Each user has a dedicated workspace containing:
  - **Datasets**: Upload and manage datasets relevant to predictive tasks.
  - **Projects**: Manage projects where trained models are stored.

## Technical Requirements

- **Technologies**: H2O.ai, Flask, Swagger, MongoDB

## Usage

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up**:
   - Follow the instructions for setting up the development environment and dependencies.

3. **Run the Application**:
   - Start the Flask server:
     ```bash
     flask run
     ```
   - Access the Swagger documentation at `http://localhost:<port>/swagger` to test the APIs.

## API Endpoints
- **Workspace Management**: Endpoints to manage user workspaces, including datasets and projects.
- **Model Training**: Endpoints to initiate the training of models using H2O.ai.
- **Model Prediction**: Endpoints to perform predictions using the trained models.
- **Model Management**: Endpoints to manage stored models in MongoDB.

