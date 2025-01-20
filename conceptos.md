# Conceptos Básicos de React

## 1. **Componentes**
Los componentes son los bloques básicos de una aplicación React. Pueden ser:
- **Funcionales:** Se definen como funciones de JavaScript y son la forma más moderna de trabajar con React.
- **De clase:** Una forma más antigua, pero también válida.

### Ejemplo:
```jsx
const MyComponent = ({ title }) => {
  return <h1>{title}</h1>;
};
```

---

## 2. **JSX (JavaScript XML)**
Una sintaxis que permite escribir código similar a HTML dentro de archivos JavaScript. Es convertido en llamadas a `React.createElement` por debajo.

### Características importantes:
- Usa `{}` para insertar valores de JavaScript.
- Todo debe estar dentro de un contenedor único como `<div>` o un fragmento `<>`.

### Ejemplo:
```jsx
const MyComponent = () => {
  return <div className="container">Hola, React!</div>;
};
```

---

## 3. **Props (Propiedades)**
Son datos que se pasan de un componente padre a uno hijo como argumentos. Son de solo lectura.

### Ejemplo:
```jsx
const Greeting = ({ name }) => {
  return <h1>Hola, {name}!</h1>;
};

<Greeting name="Ash" />;
```

---

## 4. **State (Estado)**
El estado es una forma de manejar datos internos de un componente que pueden cambiar con el tiempo. Se maneja principalmente con el hook `useState` en componentes funcionales.

### Ejemplo:
```jsx
import { useState } from 'react';

const Counter = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Cuenta: {count}</p>
      <button onClick={() => setCount(count + 1)}>Incrementar</button>
    </div>
  );
};
```

---

## 5. **Event Handling (Manejo de eventos)**
Manejo de eventos como clics, cambios, etc., con sintaxis similar al DOM pero usando camelCase.

### Ejemplo:
```jsx
const Button = () => {
  const handleClick = () => {
    alert('¡Botón presionado!');
  };

  return <button onClick={handleClick}>Presionar</button>;
};
```

---

## 6. **Rutas con React Router**
Permite manejar navegación entre páginas en aplicaciones React.

### Ejemplo:
```jsx
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

const App = () => (
  <Router>
    <nav>
      <Link to="/">Inicio</Link>
      <Link to="/about">Acerca de</Link>
    </nav>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
    </Routes>
  </Router>
);
```

---

## 7. **Hooks principales**
Funciones que permiten usar características avanzadas de React en componentes funcionales.

### Hooks importantes:
- **`useState`**: Manejo del estado local.
- **`useEffect`**: Manejo de efectos secundarios (llamadas a APIs, eventos al montar/desmontar).
- **`useContext`**: Acceso a datos globales a través del Context API.

### Ejemplo con `useEffect`:
```jsx
import { useEffect, useState } from 'react';

const FetchData = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('https://pokeapi.co/api/v2/pokemon/ditto')
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []); // [] asegura que solo se ejecute una vez al montar el componente.

  return <div>{JSON.stringify(data)}</div>;
};
```

---

## 8. **Context API**
Permite manejar estado global en una aplicación React sin necesidad de usar Redux u otras librerías externas.

### Ejemplo:
```jsx
import { createContext, useContext, useState } from 'react';

const AppContext = createContext();

const AppProvider = ({ children }) => {
  const [user, setUser] = useState('Ash Ketchum');
  return (
    <AppContext.Provider value={{ user, setUser }}>
      {children}
    </AppContext.Provider>
  );
};

const Home = () => {
  const { user } = useContext(AppContext);
  return <h1>Bienvenido, {user}!</h1>;
};

const App = () => (
  <AppProvider>
    <Home />
  </AppProvider>
);
```

---

## 9. **Llamadas a APIs**
Integrar tu app con servicios externos para obtener datos.

### Ejemplo:
```jsx
import { useEffect, useState } from 'react';

const Pokemon = () => {
  const [pokemon, setPokemon] = useState(null);

  useEffect(() => {
    fetch('https://pokeapi.co/api/v2/pokemon/pikachu')
      .then((response) => response.json())
      .then((data) => setPokemon(data));
  }, []);

  return pokemon ? <div>{pokemon.name}</div> : <p>Cargando...</p>;
};
```

---

## 10. **Ciclo de vida de un componente**
Describe las fases por las que pasa un componente React:
- **Montaje:** Cuando se renderiza por primera vez.
- **Actualización:** Cuando cambia el estado o las props.
- **Desmontaje:** Cuando el componente se elimina del DOM.

### Ejemplo con `useEffect`:
```jsx
useEffect(() => {
  console.log('Componente montado');

  return () => {
    console.log('Componente desmontado');
  };
}, []);
```

---

Con estos conceptos en mente, tienes una base sólida para avanzar en tu proyecto React. ¡Recuerda que siempre puedes volver aquí para repasar! 😊

