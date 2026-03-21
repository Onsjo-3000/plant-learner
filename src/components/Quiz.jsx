import { useState, useMemo, useCallback, useRef } from 'react';
import { getPlantsForLevel, getAllPlantsInCategory } from '../data/plants';

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function generateQuestions(categoryId, levelId) {
  const plants = getPlantsForLevel(categoryId, levelId);
  const allPlants = getAllPlantsInCategory(categoryId);

  return shuffleArray(plants).map(plant => {
    const type = Math.random() > 0.5 ? 'image-to-name' : 'name-to-image';

    const distractors = shuffleArray(
      allPlants.filter(p => p.name !== plant.name)
    ).slice(0, 3);

    const options = shuffleArray([plant, ...distractors]);

    return { plant, type, options, correctName: plant.name };
  });
}

const PLANT_EMOJIS = ['🌱', '🌿', '🍃', '🌾', '☘️', '🍀', '🌵', '🪴'];

function PlantImage({ plant, className = '' }) {
  const [error, setError] = useState(false);
  const [retries, setRetries] = useState(0);
  const emoji = PLANT_EMOJIS[plant.name.length % PLANT_EMOJIS.length];

  const handleError = useCallback(() => {
    if (retries < 2) {
      // Retry after delay (handles 429 rate limiting)
      setTimeout(() => setRetries(r => r + 1), 1000 * (retries + 1));
    } else {
      setError(true);
    }
  }, [retries]);

  return (
    <div className={`bg-gray-100 rounded-xl overflow-hidden ${className}`}>
      {error || !plant.image ? (
        <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-green-100 to-emerald-200 p-3">
          <span className="text-4xl mb-1">{emoji}</span>
          <span className="text-green-700 text-sm font-medium text-center leading-tight">{plant.name}</span>
        </div>
      ) : (
        <img
          key={retries}
          src={plant.image}
          alt=""
          className="w-full h-full object-cover"
          referrerPolicy="no-referrer"
          onError={handleError}
          loading="eager"
        />
      )}
    </div>
  );
}

export default function Quiz({ categoryId, levelId, onComplete, onBack }) {
  const questions = useMemo(() => generateQuestions(categoryId, levelId), [categoryId, levelId]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const correctRef = useRef(0);
  const [showFeedback, setShowFeedback] = useState(false);

  const question = questions[currentIndex];
  const total = questions.length;
  const isCorrect = selected === question?.correctName;

  const handleSelect = useCallback((name) => {
    if (showFeedback) return;
    setSelected(name);
    setShowFeedback(true);
    if (name === question.correctName) {
      correctRef.current += 1;
    }
  }, [showFeedback, question]);

  const handleNext = useCallback(() => {
    if (currentIndex + 1 >= total) {
      onComplete(correctRef.current);
      return;
    }
    setCurrentIndex(i => i + 1);
    setSelected(null);
    setShowFeedback(false);
  }, [currentIndex, total, onComplete]);

  if (!question) return null;

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
      {/* Header */}
      <div className="pt-4 px-4">
        <button
          onClick={onBack}
          className="text-green-600 hover:text-green-800 font-medium cursor-pointer"
        >
          ✕ Avbryt
        </button>
      </div>

      {/* Progress bar */}
      <div className="px-4 py-3 max-w-lg mx-auto">
        <div className="bg-gray-200 rounded-full h-3">
          <div
            className="bg-green-500 rounded-full h-3 transition-all duration-300"
            style={{ width: `${((currentIndex + (showFeedback ? 1 : 0)) / total) * 100}%` }}
          />
        </div>
        <p className="text-center text-sm text-gray-500 mt-1">
          {currentIndex + 1} / {total}
        </p>
      </div>

      {/* Question */}
      <div className="max-w-lg mx-auto px-4 pb-8">
        {question.type === 'image-to-name' ? (
          <>
            <h2 className="text-xl font-bold text-gray-800 text-center mb-4">
              Vilken växt är detta?
            </h2>
            <PlantImage plant={question.plant} className="w-48 h-48 mx-auto mb-6" />
            <div className="space-y-3">
              {question.options.map(opt => {
                let btnClass = 'bg-white border-2 border-gray-200 hover:border-green-400';
                if (showFeedback) {
                  if (opt.name === question.correctName) {
                    btnClass = 'bg-green-100 border-2 border-green-500 animate-pop';
                  } else if (opt.name === selected) {
                    btnClass = 'bg-red-100 border-2 border-red-500 animate-shake';
                  } else {
                    btnClass = 'bg-white border-2 border-gray-200 opacity-50';
                  }
                }
                return (
                  <button
                    key={opt.name}
                    onClick={() => handleSelect(opt.name)}
                    disabled={showFeedback}
                    className={`w-full p-4 rounded-xl text-lg font-medium text-gray-800 transition-all duration-200 cursor-pointer ${btnClass}`}
                  >
                    {opt.name}
                  </button>
                );
              })}
            </div>
          </>
        ) : (
          <>
            <h2 className="text-xl font-bold text-gray-800 text-center mb-2">
              Hitta rätt bild
            </h2>
            <p className="text-center text-2xl font-bold text-green-700 mb-6">
              {question.plant.name}
            </p>
            <div className="grid grid-cols-2 gap-3">
              {question.options.map(opt => {
                let borderClass = 'border-3 border-transparent hover:border-green-400';
                if (showFeedback) {
                  if (opt.name === question.correctName) {
                    borderClass = 'border-3 border-green-500 animate-pop';
                  } else if (opt.name === selected) {
                    borderClass = 'border-3 border-red-500 animate-shake';
                  } else {
                    borderClass = 'border-3 border-transparent opacity-50';
                  }
                }
                return (
                  <button
                    key={opt.name}
                    onClick={() => handleSelect(opt.name)}
                    disabled={showFeedback}
                    className={`rounded-xl overflow-hidden aspect-square transition-all duration-200 cursor-pointer ${borderClass}`}
                  >
                    <PlantImage plant={opt} className="w-full h-full" />
                  </button>
                );
              })}
            </div>
          </>
        )}

        {/* Feedback */}
        {showFeedback && (
          <div className={`mt-6 p-4 rounded-xl text-center ${isCorrect ? 'bg-green-100' : 'bg-red-50'}`}>
            <p className={`text-lg font-bold ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
              {isCorrect ? 'Rätt! 🎉' : `Fel! Det var ${question.correctName}`}
            </p>
            <button
              onClick={handleNext}
              className="mt-3 px-8 py-3 bg-green-600 text-white font-bold rounded-xl hover:bg-green-700 transition-colors cursor-pointer"
            >
              {currentIndex + 1 >= total ? 'Se resultat' : 'Nästa'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
