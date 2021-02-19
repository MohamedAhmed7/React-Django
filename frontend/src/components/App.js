import React, {Component} from 'react';
import {render} from 'react-dom';
import Home from './Home';
import {Link} from 'react-router-dom';


export default class App extends Component{
    constructor(props){
        super(props);

    }

    render(){
        return(
            <div>
                <h1>Hello This is my first React Django App</h1>
               
                <Home />
              
            </div>
        )
    }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);