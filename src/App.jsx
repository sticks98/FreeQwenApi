import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setContext(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      alert('Пожалуйста, введите вопрос');
      return;
    }

    setIsLoading(true);
    setResponse('');

    try {
      const content = `Контекст: ${context}; Вопрос: ${question}; Задача: Используя только контекст ответь на вопрос. Если в контексте нет информации по вопросу, тогда ответь 'Я не знаю'`;
      
      const url = "http://localhost:3264/api/chat/completions";
      const headers = {"Content-Type": "application/json"};
      const data = {
        "messages": [
          {"role": "user", "content": content}
        ],
        "model": "qwen3-max",
      };

      const response = await fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setResponse(result.choices[0].message.content);
    } catch (error) {
      console.error('Error:', error);
      setResponse('Произошла ошибка при отправке запроса: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1>Интерфейс для работы с API</h1>
        
        <form onSubmit={handleSubmit} className="api-form">
          <div className="form-group">
            <label htmlFor="context">Контекст:</label>
            <div className="context-controls">
              <input
                type="file"
                id="context-file"
                accept=".txt"
                onChange={handleFileUpload}
              />
              <span className="file-hint">Загрузите текстовый документ</span>
            </div>
            <textarea
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Загрузите текстовый документ или введите контекст вручную"
              rows="10"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="question">Вопрос:</label>
            <input
              type="text"
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Введите ваш вопрос"
              required
            />
          </div>
          
          <button type="submit" disabled={isLoading} className="submit-btn">
            {isLoading ? 'Отправка...' : 'Отправить запрос'}
          </button>
        </form>
        
        {response && (
          <div className="response-section">
            <h2>Ответ от API:</h2>
            <div className="response-content">
              {response}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;