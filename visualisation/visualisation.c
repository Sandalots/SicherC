#include "raylib.h"

int main(void)
{
  const int screenWidth = 800;
  const int screenHeight = 450;

  InitWindow(screenWidth, screenHeight, "Sicher C Compiler - Visualiser");
  SetTargetFPS(60);

  while (!WindowShouldClose())
    {
      BeginDrawing();
      ClearBackground(BLACK);
      
      DrawText("Please click the button below to input a source file you would like to be modernised and made memory-safe!", 100, 200, 12, WHITE);
      EndDrawing();
    }
  CloseWindow();

  return 0;
}
