export default function QuizResult({ correct, total, stars, passed, onRetry, onBack }) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white flex items-center justify-center px-4">
      <div className="bg-white rounded-3xl shadow-xl p-8 max-w-md w-full text-center">
        {passed ? (
          <>
            <div className="text-6xl mb-4">🎉</div>
            <h1 className="text-3xl font-bold text-green-800 mb-2">Bra jobbat!</h1>
            <p className="text-gray-600 mb-4">Du klarade nivån!</p>
          </>
        ) : (
          <>
            <div className="text-6xl mb-4">💪</div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Nästan!</h1>
            <p className="text-gray-600 mb-4">Du behöver minst {total - 1} rätt för att klara nivån</p>
          </>
        )}

        <div className="bg-gray-50 rounded-2xl p-6 mb-6">
          <p className="text-5xl font-bold text-green-700 mb-2">{correct}/{total}</p>
          <p className="text-gray-500">rätt svar</p>
          {passed && (
            <div className="mt-3 text-3xl">
              {[1, 2, 3].map(i => (
                <span key={i} className={i <= stars ? 'text-yellow-400' : 'text-gray-300'}>
                  ★
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-3">
          {!passed && (
            <button
              onClick={onRetry}
              className="w-full py-3 bg-green-600 text-white font-bold rounded-xl hover:bg-green-700 transition-colors cursor-pointer"
            >
              Försök igen
            </button>
          )}
          {passed && (
            <button
              onClick={onRetry}
              className="w-full py-3 bg-green-100 text-green-700 font-bold rounded-xl hover:bg-green-200 transition-colors cursor-pointer"
            >
              Gör om för fler stjärnor
            </button>
          )}
          <button
            onClick={onBack}
            className="w-full py-3 bg-gray-100 text-gray-700 font-bold rounded-xl hover:bg-gray-200 transition-colors cursor-pointer"
          >
            Tillbaka till nivåer
          </button>
        </div>
      </div>
    </div>
  );
}
