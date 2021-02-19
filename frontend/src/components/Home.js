import React, {Component} from 'react';
import {render} from 'react-dom';
import CreateRoom from './CreateRoom';
import JoinRoom from './JoinRoom';
import { BrowserRouter as Router, Switch, Route, Link, Redirect} from 'react-router-dom';
export default class Home extends Component{
    constructor(props){
        super(props);

    }

    render(){
        return(
            <Router>
                
                <Switch>
                    <Route exact path='/' ><p>Home Page</p></Route>
                    <Route path='/join' component={JoinRoom} />
                    <Route path='/create' component={CreateRoom} />
                </Switch>
            </Router>
        )
    }
}
