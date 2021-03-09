import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
    return (
        <button
            className="square"
            onClick={() => props.onClick()}
        >
            {props.value === 0 ? " " : props.value}
        </button>
    );
}


class Board extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            squares: Array(9).fill(null),
            blank: null,
        };
    }

    componentDidMount() {
        fetch('/initial').then(res => res.json()).then(data => {
            this.setState({
                squares: data,
                blank: data.indexOf(0),
                solution: null
            });
        });
    }

    handleClick(i) {
        const blank = this.state.blank;
        const diff = i - blank;

        if ([1, 3].includes(Math.abs(diff))) {
            const squares = this.state.squares.slice();
            squares[i] = 0;
            squares[this.state.blank] = this.state.squares[i]

            this.setState({ squares: squares, blank: i });
        }

    }

    handleNew() {
        fetch('/initial').then(res => res.json()).then(data => {
            this.setState({
                squares: data,
                blank: data.indexOf(0),
                solution: null
            });
        });
    }

    handleSolve() {
        fetch('/solution', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.state.squares)
        }).then(res => res.json()).then(data => {
            this.setState({
                solution: data,
                blank: data.indexOf(0)
            });
        });
    }

    renderSquare(i) {
        return (
            <Square
                value={this.state.squares[i]}
                onClick={() => this.handleClick(i)}
            />
        );
    }

    render() {

        return (
            <div>
                <button className='tool' onClick={() => this.handleNew()}>New</button>
                <button className='tool' onClick={() => this.handleSolve()}>Solve</button>
                <div className="board-row">
                    {this.renderSquare(0)}
                    {this.renderSquare(1)}
                    {this.renderSquare(2)}
                </div>
                <div className="board-row">
                    {this.renderSquare(3)}
                    {this.renderSquare(4)}
                    {this.renderSquare(5)}
                </div>
                <div className="board-row">
                    {this.renderSquare(6)}
                    {this.renderSquare(7)}
                    {this.renderSquare(8)}
                </div>
                {this.state.solution && (
                    <div className="game-info">
                        <div><h3>Action Sequence:</h3></div>
                        <ol>{this.state.solution.map((action, index) => (
                            <li key={index}>{action}</li>
                        ))
                        }</ol>
                    </div>
                )}
            </div>

        );
    }
}

class Game extends React.Component {
    render() {
        return (
            <div className="game">
                <div className="game-board">
                    <Board />
                </div>
                
            </div>
        );
    }
}

// ========================================

ReactDOM.render(
    <Game />,
    document.getElementById('root')
);
