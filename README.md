# Cookbooks page
## Project Overview
This is a school project. The purpose of this application is to create a web app using a relational database (MySQL) to manage recipes and cookbooks. The app allows users to:
- Manage recipes and cookbooks
- Assign recipes to cookbooks
- Import recipes and cookbooks from JSON files
### Author:
Sofia Hennelová, sofia.hennelova@gmail.com
### School: 
Secondary Technical School of Electrical Engineering Jecna 30, Prague
### Date: 
2\. 1\. 2026

## Installation and configuration

### Database

1. Create a `recipe_project` schema in MySQL. For example, in MySQL Workbench:
```sql
CREATE DATABASE recipe_project;
```
2. Make sure your MySQL server is running and accessible.

### Backend

1. Navigate to the backend folder
2. Open in terminal
3. Create and activate a virtual environment:
```powershell
py -m venv .venv
.venv\Scripts\activate
```
4. Upgrade pip and install dependencies:
```powershell
py -m pip install --upgrade pip
py -m pip install flask flask-cors mysql-connector-python
```
5. Set up `config.json`
```
{
  "mysql": {
    "host": "127.0.0.1",
    "user": "username",
    "password": "password",
    "database": "recipe_project"
  }
}
```
6. Run the backend server:
```powershell
py main.py
```

### Frontend

1. Navigate to the frontend folder
2. Install Node.js dependencies:
```powershell
npm install
```
3. Run the frontend dev server:
```powershell
npm run dev
```

## Importing Data
Recipes and cookbooks can be imported from JSON files via the web UI.
### Recipe JSON format
```json
    {
      "recipes": [
        {
          "title": "Title",
          "description": "Description",
          "difficulty": "easy|medium|hard",
          "is_vegetarian": false,
          "ingredients": [
            {"name": "Name", "amount": 200, "unit": "g"},
            {"name": "Name", "amount": 300, "unit": "g"}
          ]
        }
      ]
    }
```
### Cookbook JSON format
```json
    {
      "cookbooks": [
        {"name": "Name", "description": "Description"},
        {"name": "Name", "description": "Description"}
      ]
    }
```
## Non-functional requirements
### Backend (Python)
- flask 
- flask-cors
- mysql-connector-python 

### Frontend (React/Node.js)
- react 
- react-dom
- npm

### Database
- MySQL server

## Functional Requirements
The application must:
- Use a real relational database (MySQL)
- Support at least 5 tables (including junction tables)
- Include at least 2 views
- Include at least 1 many-to-many relationship
- Cover all required data types: float, boolean, enum, string, datetime
- Allow insert, update, delete, and view operations across multiple tables
- Use transactions where needed (e.g., adding recipe with ingredients)
- Generate a summary report with aggregated data
- Allow import from JSON into at least 2 tables
- Handle invalid input and errors in a user-friendly way

## Architecture
The application follows a **layered architecture**:
- **Database Layer**: MySQL with tables: `recipe`, `ingredient`, `recipe_ingredient`, `cookbook`, `recipe_cookbook`  
  - Views: `view_recipe_details`, `view_cookbook_summary`  
- **Repository Layer**: Handles direct SQL queries  
- **Service Layer**: Business logic, transactions, validations  
- **API Layer**: Flask REST API endpoints  
- **Frontend**: React application to interact with the API  

## Database Schema
![Database Schema](./images/ER.png)

## Behavioral diagram
### Recipe Management
![Activity diagram – Recipe Management](./images/Recipe.png)
### Cookbook Management
![Activity diagram – Cookbook Management](./images/Cookbook.png)




