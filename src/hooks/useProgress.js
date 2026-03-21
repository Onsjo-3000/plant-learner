import { useState, useCallback } from 'react';

const STORAGE_KEY = 'plant-learner-progress';

function loadProgress() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : {};
  } catch {
    return {};
  }
}

function saveProgress(progress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

export function useProgress() {
  const [progress, setProgress] = useState(loadProgress);

  // Hämta resultat för en specifik nivå: { stars, completed }
  const getLevelProgress = useCallback((categoryId, levelId) => {
    const key = `${categoryId}-${levelId}`;
    return progress[key] || { stars: 0, completed: false };
  }, [progress]);

  // Kolla om en nivå är upplåst
  const isLevelUnlocked = useCallback((categoryId, levelId) => {
    if (levelId === 1) return true;
    const prevKey = `${categoryId}-${levelId - 1}`;
    return progress[prevKey]?.completed || false;
  }, [progress]);

  // Spara resultat för en nivå
  const completLevel = useCallback((categoryId, levelId, correctCount, totalCount) => {
    const stars = correctCount === totalCount ? 3 : correctCount >= totalCount - 1 ? 2 : 1;
    const passed = correctCount >= totalCount - 1; // Minst 4/5

    if (!passed) return { stars: 0, passed: false };

    setProgress(prev => {
      const key = `${categoryId}-${levelId}`;
      const existing = prev[key];
      // Behåll bästa resultat
      const bestStars = existing ? Math.max(existing.stars, stars) : stars;
      const next = { ...prev, [key]: { stars: bestStars, completed: true } };
      saveProgress(next);
      return next;
    });

    return { stars, passed: true };
  }, []);

  // Räkna framsteg per kategori
  const getCategoryProgress = useCallback((categoryId, totalLevels) => {
    let completed = 0;
    let totalStars = 0;
    for (let i = 1; i <= totalLevels; i++) {
      const p = progress[`${categoryId}-${i}`];
      if (p?.completed) {
        completed++;
        totalStars += p.stars;
      }
    }
    return { completed, totalLevels, totalStars, maxStars: totalLevels * 3 };
  }, [progress]);

  const resetProgress = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setProgress({});
  }, []);

  return { getLevelProgress, isLevelUnlocked, completLevel, getCategoryProgress, resetProgress };
}
