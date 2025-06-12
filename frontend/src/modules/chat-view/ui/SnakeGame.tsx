import React, { useEffect, useRef, useState } from "react";

const BOARD_SIZE = 12;
const INITIAL_SNAKE = [
  { x: 5, y: 6 },
  { x: 4, y: 6 },
];
const INITIAL_DIRECTION = { x: 1, y: 0 };
const SPEED = 120;

function getRandomFood(snake: { x: number; y: number }[]) {
  let food: { x: number; y: number };
  do {
    food = {
      x: Math.floor(Math.random() * BOARD_SIZE),
      y: Math.floor(Math.random() * BOARD_SIZE),
    };
  } while (snake.some((s) => s.x === food.x && s.y === food.y));
  return food;
}

export const SnakeGame: React.FC = () => {
  const [snake, setSnake] = useState(INITIAL_SNAKE);
  const [direction, setDirection] = useState(INITIAL_DIRECTION);
  const [food, setFood] = useState(getRandomFood(INITIAL_SNAKE));
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const moveRef = useRef(direction);
  const running = useRef(true);

  useEffect(() => {
    moveRef.current = direction;
  }, [direction]);

  useEffect(() => {
    if (gameOver) return;
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowUp" && moveRef.current.y !== 1)
        setDirection({ x: 0, y: -1 });
      if (e.key === "ArrowDown" && moveRef.current.y !== -1)
        setDirection({ x: 0, y: 1 });
      if (e.key === "ArrowLeft" && moveRef.current.x !== 1)
        setDirection({ x: -1, y: 0 });
      if (e.key === "ArrowRight" && moveRef.current.x !== -1)
        setDirection({ x: 1, y: 0 });
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [gameOver]);

  useEffect(() => {
    if (gameOver) return;
    const interval = setInterval(() => {
      setSnake((prev) => {
        const newHead = {
          x: (prev[0].x + moveRef.current.x + BOARD_SIZE) % BOARD_SIZE,
          y: (prev[0].y + moveRef.current.y + BOARD_SIZE) % BOARD_SIZE,
        };
        if (prev.some((s) => s.x === newHead.x && s.y === newHead.y)) {
          setGameOver(true);
          running.current = false;
          return prev;
        }
        let newSnake = [newHead, ...prev];
        if (newHead.x === food.x && newHead.y === food.y) {
          setFood(getRandomFood(newSnake));
          setScore((s) => s + 1);
        } else {
          newSnake.pop();
        }
        return newSnake;
      });
    }, SPEED);
    return () => clearInterval(interval);
  }, [food, gameOver]);

  const restart = () => {
    setSnake(INITIAL_SNAKE);
    setDirection(INITIAL_DIRECTION);
    setFood(getRandomFood(INITIAL_SNAKE));
    setScore(0);
    setGameOver(false);
    running.current = true;
  };

  return (
    <div className="flex flex-col items-center">
      <div className="mb-2 text-lg font-semibold">Змейка! Счет: {score}</div>
      <div
        className="grid bg-gray-900 rounded-md"
        style={{
          gridTemplateRows: `repeat(${BOARD_SIZE}, 1.5rem)`,
          gridTemplateColumns: `repeat(${BOARD_SIZE}, 1.5rem)`,
        }}
      >
        {[...Array(BOARD_SIZE * BOARD_SIZE)].map((_, i) => {
          const x = i % BOARD_SIZE;
          const y = Math.floor(i / BOARD_SIZE);
          const isSnake = snake.some((s) => s.x === x && s.y === y);
          const isHead = snake[0].x === x && snake[0].y === y;
          const isFood = food.x === x && food.y === y;
          return (
            <div
              key={i}
              className={
                "border border-gray-800 flex items-center justify-center " +
                (isHead
                  ? "bg-green-400"
                  : isSnake
                  ? "bg-green-200"
                  : isFood
                  ? "bg-red-400"
                  : "bg-gray-950")
              }
            >
              {isFood ? "🍎" : ""}
            </div>
          );
        })}
      </div>
      {gameOver && (
        <div className="mt-3 text-center">
          <div className="text-red-500 font-bold mb-2">Игра окончена!</div>
          <button
            className="px-4 py-2 rounded bg-black text-white hover:bg-gray-800 transition"
            onClick={restart}
          >
            Рестарт
          </button>
        </div>
      )}
      <div className="mt-2 text-xs text-gray-500">
        Управление: стрелки на клавиатуре
      </div>
    </div>
  );
};
