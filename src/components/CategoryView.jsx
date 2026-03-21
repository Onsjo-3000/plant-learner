import { categories } from '../data/plants';

function Stars({ count }) {
  return (
    <span className="text-sm">
      {[1, 2, 3].map(i => (
        <span key={i} className={i <= count ? 'text-yellow-400' : 'text-gray-300'}>★</span>
      ))}
    </span>
  );
}

export default function CategoryView({ categoryId, onBack, onStartLevel, getLevelProgress, isLevelUnlocked }) {
  const category = categories.find(c => c.id === categoryId);
  if (!category) return null;

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
      <header className="pt-6 pb-4 px-4">
        <button
          onClick={onBack}
          className="text-green-600 hover:text-green-800 font-medium mb-4 inline-flex items-center gap-1 cursor-pointer"
        >
          ← Tillbaka
        </button>
        <div className="text-center">
          <span className="text-5xl mb-2 block">{category.icon}</span>
          <h1 className="text-3xl font-bold text-green-800">{category.name}</h1>
          <p className="text-green-600">{category.description}</p>
        </div>
      </header>

      <div className="max-w-md mx-auto px-4 pb-12">
        <div className="relative">
          {/* Connecting line */}
          <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-green-200 -translate-x-1/2 z-0" />

          <div className="relative z-10 space-y-6 pt-4">
            {category.levels.map((level, index) => {
              const unlocked = isLevelUnlocked(categoryId, level.id);
              const prog = getLevelProgress(categoryId, level.id);

              return (
                <div key={level.id} className="flex flex-col items-center">
                  <button
                    onClick={() => unlocked && onStartLevel(categoryId, level.id)}
                    disabled={!unlocked}
                    className={`
                      w-20 h-20 rounded-full flex items-center justify-center text-2xl font-bold
                      shadow-lg transition-all duration-200 cursor-pointer
                      ${unlocked
                        ? prog.completed
                          ? 'bg-gradient-to-br from-yellow-400 to-yellow-500 text-white hover:scale-110'
                          : 'bg-gradient-to-br from-green-400 to-green-600 text-white hover:scale-110'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                      }
                    `}
                  >
                    {unlocked ? (prog.completed ? '✓' : level.id) : '🔒'}
                  </button>
                  <h3 className={`mt-2 font-semibold ${unlocked ? 'text-gray-800' : 'text-gray-400'}`}>
                    {level.name}
                  </h3>
                  <p className="text-sm text-gray-500">{level.plants.length} växter</p>
                  {prog.completed && <Stars count={prog.stars} />}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
