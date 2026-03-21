import { categories } from '../data/plants';

export default function Home({ onSelectCategory, getCategoryProgress }) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
      <header className="pt-8 pb-6 px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-green-800 mb-2">
          Växtläraren
        </h1>
        <p className="text-green-600 text-lg">Lär dig känna igen växter - en nivå i taget</p>
      </header>

      <div className="max-w-4xl mx-auto px-4 pb-12">
        <h2 className="text-xl font-semibold text-gray-700 mb-6 text-center">Välj en kategori</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map(cat => {
            const prog = getCategoryProgress(cat.id, cat.levels.length);
            return (
              <button
                key={cat.id}
                onClick={() => onSelectCategory(cat.id)}
                className={`relative overflow-hidden rounded-2xl bg-gradient-to-br ${cat.color} p-6 text-white shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 text-left cursor-pointer`}
              >
                <div className="text-4xl mb-3">{cat.icon}</div>
                <h3 className="text-xl font-bold mb-1">{cat.name}</h3>
                <p className="text-white/80 text-sm mb-3">{cat.description}</p>

                {/* Progress bar */}
                <div className="bg-white/30 rounded-full h-2 mb-1">
                  <div
                    className="bg-white rounded-full h-2 transition-all duration-500"
                    style={{ width: `${(prog.completed / prog.totalLevels) * 100}%` }}
                  />
                </div>
                <p className="text-white/80 text-xs">
                  {prog.completed}/{prog.totalLevels} nivåer klara
                  {prog.totalStars > 0 && ` · ${'⭐'.repeat(1)} ${prog.totalStars}/${prog.maxStars}`}
                </p>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
