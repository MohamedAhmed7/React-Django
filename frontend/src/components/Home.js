import React, {Component} from 'react';
import {render} from 'react-dom';
import CreateRoom from './CreateRoom';
import JoinRoom from './JoinRoom';
import Room from './Room';
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
                    <Route path='/room/:roomCode' component={Room} />
                </Switch>
            </Router>
        )
    }
}
