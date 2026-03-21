import { useState, useCallback } from 'react';
import { useProgress } from './hooks/useProgress';
import Home from './components/Home';
import CategoryView from './components/CategoryView';
import Quiz from './components/Quiz';
import QuizResult from './components/QuizResult';

export default function App() {
  const [screen, setScreen] = useState('home'); // home | category | quiz | result
  const [currentCategory, setCurrentCategory] = useState(null);
  const [currentLevel, setCurrentLevel] = useState(null);
  const [quizResult, setQuizResult] = useState(null);

  const { getLevelProgress, isLevelUnlocked, completLevel, getCategoryProgress } = useProgress();

  const handleSelectCategory = useCallback((categoryId) => {
    setCurrentCategory(categoryId);
    setScreen('category');
  }, []);

  const handleStartLevel = useCallback((categoryId, levelId) => {
    setCurrentCategory(categoryId);
    setCurrentLevel(levelId);
    setScreen('quiz');
  }, []);

  const handleQuizComplete = useCallback((correctCount) => {
    const total = 5;
    const result = completLevel(currentCategory, currentLevel, correctCount, total);
    setQuizResult({ correct: correctCount, total, ...result });
    setScreen('result');
  }, [currentCategory, currentLevel, completLevel]);

  const handleRetry = useCallback(() => {
    setScreen('quiz');
    setQuizResult(null);
  }, []);

  const handleBackToCategory = useCallback(() => {
    setScreen('category');
    setQuizResult(null);
  }, []);

  switch (screen) {
    case 'home':
      return (
        <Home
          onSelectCategory={handleSelectCategory}
          getCategoryProgress={getCategoryProgress}
        />
      );
    case 'category':
      return (
        <CategoryView
          categoryId={currentCategory}
          onBack={() => setScreen('home')}
          onStartLevel={handleStartLevel}
          getLevelProgress={getLevelProgress}
          isLevelUnlocked={isLevelUnlocked}
        />
      );
    case 'quiz':
      return (
        <Quiz
          key={`${currentCategory}-${currentLevel}-${Date.now()}`}
          categoryId={currentCategory}
          levelId={currentLevel}
          onComplete={handleQuizComplete}
          onBack={handleBackToCategory}
        />
      );
    case 'result':
      return (
        <QuizResult
          correct={quizResult.correct}
          total={quizResult.total}
          stars={quizResult.stars}
          passed={quizResult.passed}
          onRetry={handleRetry}
          onBack={handleBackToCategory}
        />
      );
    default:
      return null;
  }
}
