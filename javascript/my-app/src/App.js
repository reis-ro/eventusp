import './App.css';
import React from "react";

function MoviesTable(props) {
  const {list, onDismiss, searchTerm} = props;
  return (
    <table>
        <thead>
          <tr>
            <th>Id</th>
            <th>Título</th>
            <th>Data</th>
            <th>URL da Capa</th>
          </tr>
        </thead>
        <tbody>
          {list.filter(movie => movie.name.toLowerCase().includes(searchTerm.toLowerCase()))
          .map((movie) => (
            <tr key={movie.id}>
              <td>{movie.id}</td>
              <td>{movie.name}</td>
              <td>{movie.date}</td>
              <td>{movie.event_photo_url}</td>
              <td>
                <Button onClick ={() => onDismiss(movie.id)}>
                  Dismiss
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
  );
}

function Search(props) {
  const {searchTerm, handleInputChange, children} = props;
  return (
      <form>
        {children} <input type="text" placeholder="Search by movie name"
          name="searchTerm" value={searchTerm} 
          onChange={(event) => handleInputChange(event)}/>
      </form>
    );
}

function Button(props) {
  const {
    onClick,
    className='',
    children,
  } = props;

  return (
    <button
      onClick={onClick}
      className={className}
      type="button"
    >
      {children}
    </button>
  );
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { list: null, searchTerm:''};
  }

  handleInputChange(event) {
    const target = event.target;
    const value = 
      target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  onDismiss(id) {
    const updatedList = this.state.list.filter(item => item.id !== id);
    this.setState({ list: updatedList });
  }

  onSearchChange(event) {
    this.setState({ searchTerm: event.target.value });
  }

  componentDidMount() {
    fetch('http://127.0.0.1:8000/api/v1/events/')
      .then((response) => response.json())
      .then((result) => this.setState({ list: result }))
      .catch((error) => error);
  }

  render() {
    const {list, searchTerm} = this.state;
    
    return (
      <div className="App">
        <Search
          searchTerm={searchTerm}
          handleInputChange={(e) => this.handleInputChange(e)}
        >
          Search term:
        </Search>
        { list && (
          <MoviesTable 
            list={list} 
            searchTerm={searchTerm}
            onDismiss={(id) => this.onDismiss(id)}
          />
        )}
      </div>
    );
  }
}

export default App;
