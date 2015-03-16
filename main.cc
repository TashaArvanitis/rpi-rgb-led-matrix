#include "thread.h"
#include "led-matrix.h"

#include <assert.h>
#include <unistd.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>

using std::min;
using std::max;

// Base-class for a Thread that does something with a matrix.
class RGBMatrixManipulator : public Thread {
  public:
    RGBMatrixManipulator(RGBMatrix *m) : running_(true), matrix_(m) {}
    virtual ~RGBMatrixManipulator() { running_ = false; }

    // Run() implementation needs to check running_ regularly.

  protected:
    volatile bool running_;  // TODO: use mutex, but this is good enough for now.
    RGBMatrix *const matrix_;
};

// Pump pixels to screen. Needs to be high priority real-time because jitter
// here will make the PWM uneven.
class DisplayUpdater : public RGBMatrixManipulator {
  public:
    DisplayUpdater(RGBMatrix *m) : RGBMatrixManipulator(m) {}

    void Run() {
      while (running_) {
        matrix_->UpdateScreen();
      }
    }
};

// -- The following are demo image generators.


class SuperSimpleSadness : public RGBMatrixManipulator {
  public:
    SuperSimpleSadness(RGBMatrix *m) : RGBMatrixManipulator(m) {}
    void Run() {
      const int width = matrix_->width();
      const int height = matrix_->height();
      uint32_t count = 0;
      while (running_) {
        usleep(5000);
        ++count;

        if (count % 2 == 0) {
          r = g = b = 50;
        } else {
          r = g = b = 255;
        }

        for (int x = 0; x < width; ++x)
          for (int y = 0; y < height; ++y)
            matrix_->SetPixel(x, y, r, g, b);

      }
    }
};



int main(int argc, char *argv[]) {
  GPIO io;
  if (!io.Init())
    return 1;

  RGBMatrix m(&io);

  RGBMatrixManipulator *image_gen = NULL;
  image_gen = new SuperSimpleSadness(&m);

  if (image_gen == NULL)
    return 1;

  RGBMatrixManipulator *updater = new DisplayUpdater(&m);
  updater->Start(10);  // high priority

  image_gen->Start();

  // Things are set up. Just wait for <RETURN> to be pressed.
  printf("Press <RETURN> to exit and reset LEDs\n");
  getchar();

  // Stopping threads and wait for them to join.
  delete image_gen;
  delete updater;

  // Final thing before exit: clear screen and update once, so that
  // we don't have random pixels burn
  m.ClearScreen();
  m.UpdateScreen();

  return 0;
}
