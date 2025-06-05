import { useEffect, useState } from "react";
import { db } from "./firebase";
import { collection, onSnapshot, addDoc } from "firebase/firestore";

interface Todo {
  id: string;
  content: string;
}

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);

  useEffect(() => {
    const unsubscribe = onSnapshot(collection(db, "todos"), (snapshot) => {
      setTodos(
        snapshot.docs.map((doc) => ({
          id: doc.id,
          ...(doc.data() as Omit<Todo, "id">),
        }))
      );
    });
    return unsubscribe;
  }, []);

  function createTodo() {
    const content = window.prompt("Todo content");
    if (content) {
      addDoc(collection(db, "todos"), { content });
    }
  }

  return (
    <main>
      <h1>My todos</h1>
      <button onClick={createTodo}>+ new</button>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>{todo.content}</li>
        ))}
      </ul>
      <div>Todo data is stored in Firebase Firestore.</div>
    </main>
  );
}

export default App;
