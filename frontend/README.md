### Getting Started with React Vite
* The project is based on Vite to enable a faster development experience
* You can create a project using the following command:
npm create vite@latest my-react-app --template react

### Project Information
* Project description
* Project version

### How To Run The Application
* Clone this repository into your local machine
* Run (npm install or npm i) to install the project dependencies
* Run (npm run dev) and the project will be automatically available at (localhost:3000)

### How To Build The Application
* Run (npm run build) to get the dist folder which includes the built files

### How To Change The Port
* Go to the config folder then to the server.json file and change the port property inside of the server object

### Main Project Dependencies
* Axios: As an http library
* React Bootstrap: As a styling library
* React Router: As a routing library
* Line Awesome: As icons library
* Redux Toolkit: As a state management library

### Project Structure
The structure is based on the recommended redux toolkit 2022 folders structure
* Config Folder: Includes the needed config files for the application (ex: endpoint url)
* API Folder: Includes the Js files that handle the communication with the backend
* App Folder: Includes the store file (redux-toolkit store) - App.Jsx file (the main component) - app.css (The global app styles)
* Common Folder: Includes the common components folder and the utilities folder
* Images Folder: Includes the project images
* Localization Folder: Includes the localization Json files
* Features Folder: Each project feature will be inside a folder which includes the components folder and the reducer file and the styling file
* Main File: The entry point of the project
