// Shriya Vohra, 05-29-14
// Simple version of the popular Othello board game.
// Enjoy!

#include <iostream>
#include <windows.h>
#include <stdio.h>

COORD coord = {0,0};

using namespace std;

void gotoxy(int x, int y) {
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),coord);
}

class Piece {
    private:
        int color;      // 0 = green, 1 = red, 2 = undecided
        int x, y;
    public:
        Piece();
        void setColor (int c) { color = c; }
        void set (int xPos, int yPos, int c) {
            x = xPos;
            y = yPos;
            color = c;
        }
        void set (int xPos, int yPos) {
            x = xPos;
            y = yPos;
        }
        int getColor() {return color;}
        int getX() {return x;}
        int getY() {return y;}
        void display();
};

Piece::Piece() {
    // Default x,y not on board
    // Default color = undecided
    x = -1;
    y = -1;
    color = 2;
}

void Piece::display() {
    if (color == 0) {
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),10);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),6986);
        cout << " G ";
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),15);
    } else if (color == 1) {
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),12);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),6988);
        cout << " R ";
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),15);
    } else {
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),6991);
        cout << " - ";
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),15);
    }
}

class Board {
    private:
        Piece list[64];
        int x1, y1;
        int status, redpiece, blackpiece, winner;
        int inRange(int x, int y);
        int pieceAtLoc(int x, int y);
        int validPlacement(int x, int y);
        void flip(int posi, int color);
        void display();
        void move();
    public:
        Board();
        void execute();
};

Board::Board() {
    for (int i = 1; i < 65; i++) {
        list[i].setColor(2);
    }
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),15);
    int j = 1;
    cout << endl << endl << "\t\t\t";
    for (int i = 1; i <= 8; i++) {
        cout << "  " << i;
    }
    cout << endl << "\t\t\t" << j;
    j++;
    for (int i = 1; i < 65; i++) {
        list[i].display();
        if (i % 8 == 0 && i != 0 && j != 9) {
            cout << endl << "\t\t\t" << j;
            j++;
        }
    }

    cout << endl << endl << endl;
}

int Board::pieceAtLoc(int x, int y) {
    int pos;
    int clr;

    if (x == 1) {
        pos = x*y;
        clr = list[pos].getColor();
        if (clr != 2) {
            cout << "There is already a piece there. Invalid.";
            return 1;
        } else {
            return 0;
        }
    } else {
        pos = 8*x - (8-y);
        clr = list[pos].getColor();
        cout << "pos " << pos << "clr " << clr << endl;
        if (clr != 2) {
            clr = 2;
            list[pos].setColor(2);
            return 0;
        } else {
            return 0;
        }
    }
}

int Board::inRange(int x, int y) {
    if (x > 8 || y > 8) {
        cout << endl << "Invalid coordinates.";
        return 1;
    } else if (x < 1 || y < 1) {
        cout << endl << "Invalid coordinates.";
        return 1;
    } else {
        return 0;
    }
}

void Board::flip(int post, int col) {
    list[post].setColor(col);
}

int Board::validPlacement(int x, int y) {
    bool otherClr = true;  // See if it works
    bool final = false;
    int pos;
    if (x==1) {
        pos = x*y;
    } else {
        pos = 8*x - (8-y);
    }


    // Look left
    int counter = y+1;  // Check for color with one after the orig coord
    int tempPos;
    int tempClr;
    while (counter <= 8 && y != 8) {
        if (x==1) {
            tempPos = x*counter;
        } else {
            tempPos = 8*x - (8-counter);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr = false;
            break;
        }
        if (counter == y+1 && tempClr == status) {
            otherClr = false;
            break;
        } else if (tempClr == status) {
            otherClr = true;
            final = true;
            for (int i = pos+1; i < tempPos; i++) {
                flip(i,status);
            }
            break;
        }
        counter++;
    }


    // Look right
    bool otherClr2 = true;
    counter = y-1;  // Check for color with one after the orig coord
    tempPos;
    tempClr;
    while (counter >= 1 && y!=1) {
        if (x==1) {
            tempPos = x*counter;
        } else {
            tempPos = 8*x - (8-counter);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr2 = false;
            break;
        }
        if (counter == y-1 && tempClr == status) {
            otherClr2 = false;
            break;
        } else if (tempClr == status) {
            otherClr2 = true;
            final = true;
            for (int i = pos-1; i > tempPos; i--) {
                flip(i,status);
            }
            break;
        }
        counter--;
    }


    // Look up
    bool otherClr3 = true;
    counter = x-1;  // Check for color with one after the orig coord
    while (counter >= 1) {
        if (x!=1) {
            tempPos = 8*counter - (8-y);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr3 = false;
            break;
        }
        if (counter == x-1 && tempClr == status) {
            otherClr3 = false;
            break;
        } else if (tempClr == status) {
            otherClr3 = true;
            final = true;
            for (int i = pos-8; i > tempPos; i = i-8) {
                flip(i,status);
            }
            break;
        }
        counter--;
    }

    // Look down
    bool otherClr4 = true;
    counter = x+1;  // Check for color with one after the orig coord
    while (counter <= 8) {
        if (x!=8) {
            tempPos = 8*counter - (8-y);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr4 = false;
            break;
        }
        if (counter == x+1 && tempClr == status) {
            break;
            otherClr4 = false;
        } else if (tempClr == status) {
            otherClr4 = true;
            final = true;
            for (int i = pos+8; i < tempPos; i = i+8) {
                flip(i,status);
            }
            break;
        }
        counter++;
    }

    // ---------------------------------------------------------------------------------------------
    // -------------------- DIAGONALS ----------------------

    // Look NE
    int counterY = y+1;  // Check for color with one after the orig coord
    int counterX = x-1;
    while (counterY <= 8 && counterX >= 1) {
        if (x==1) {
            tempPos = (counterX)*counterY;
        } else {
            tempPos = 8*counterX - (8-counterY);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr = false;
            break;
        }
        if (counterY == y+1 && tempClr == status) {
            break;
            otherClr = false;
        } else if (tempClr == status) {
            otherClr = true;
            final = true;
            for (int i = pos; i > tempPos; i = i-7) {
                flip(i,status);
            }
            break;
        }
        counterY++;
        counterX--;
    }

    // Look SW
    //otherClr = false;
    counterY = y-1;  // Check for color with one after the orig coord
    counterX = x+1;
    while (counterY >= 1 && counterX <= 8) {
        if (x==1) {
            tempPos = (counterX)*counterY;
        } else {
            tempPos = 8*counterX - (8-counterY);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr = false;
            break;
        }
        if (counterY == y-1 && tempClr == status) {
            break;
            otherClr = false;
        } else if (tempClr == status) {
            otherClr = true;
            final = true;
            for (int i = pos; i < tempPos; i = i+7) {
                flip(i,status);
            }
            break;
        }
        counterY--;
        counterX++;
    }

    // Look SE
    counterY = y+1;  // Check for color with one after the orig coord
    counterX = x+1;
    while (counterY <= 8 && counterX <= 8) {
        if (x==1) {
            tempPos = (counterX)*counterY;
        } else {
            tempPos = 8*counterX - (8-counterY);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr = false;
            break;
        }
        if (counterY == y+1 && tempClr == status) {
            break;
            otherClr = false;
        } else if (tempClr == status) {
            otherClr = true;
            final = true;
            for (int i = pos; i < tempPos; i = i+9) {
                flip(i,status);
            }
            break;
        }
        counterY++;
        counterX++;
    }

    // Look NW
    counterY = y-1;  // Check for color with one after the orig coord
    counterX = x-1;
    while (counterY >= 1 && counterX >= 1) {
        if (x==1) {
            tempPos = (counterX)*counterY;
        } else {
            tempPos = 8*counterX - (8-counterY);
        }

        tempClr = list[tempPos].getColor();

        // If one next to it is same color, quit.
        if (tempClr == 2) {
            otherClr = false;
            break;
        }
        if (counterY == y+1 && tempClr == status) {
            break;
            otherClr = false;
        } else if (tempClr == status) {
            otherClr = true;
            final = true;
            for (int i = pos; i > tempPos; i = i-9) {
                flip(i,status);
            }
            break;
        }
        counterY--;
        counterX--;
    }

    // --------------------------------------------------------------------------------------
    // --------------- END DIAGONALS --------------------

    if (final) {
        list[pos].setColor(status);
        return 0;
    } else {
        return 1;
    }

}

void Board::move() {
    int oldClr = list[64].getColor();
    bool xisone = false;
    // Input coordinates
    cout << "Enter coordinates below or '10' to pass." << endl;
    cout << "Enter row #: ";
    cin >> x1;

    if (x1 == 10) {
        cout << endl << "You have chosen to pass. Switching turns..." << endl;
        return;
    } else if (x1 == 1) {
        xisone = true;
        list[64].setColor(oldClr);
    }

    cout << "Enter column #: ";
    cin >> y1;

    // When x = 1, (8,8) automatically changes to R!!
    // If changed back, x becomes 2!!
    if (xisone) {
        x1 = 1;
    }

    int pieceThere = -1;
    int withinRange = inRange(x1,y1);
    if (withinRange == 1) {
        if (status == 0) {
            status++;
        } else {
            status = 0;
        }
        return;
    }
    int trapPiece;
    if (withinRange == 0) {pieceThere = pieceAtLoc(x1,y1);}
    if (pieceThere == 0) {trapPiece = validPlacement(x1,y1);}
    list[64].setColor(0);
    list[63].setColor(0);

    if (trapPiece == 1) {
        // Reenter correct coordinates
        cout << "You are not trapping a piece! Reenter coordinates." << endl;
        if (status == 0) {
            status++;
        } else {
            status = 0;
        }
        return;
    }

    if (pieceThere == 0 && withinRange == 0 && trapPiece == 0) {
        // Place piece there
        int position;
        if (x1 == 1) {
            position = x1*y1;
            list[position].setColor(status);
        } else {
            position = 8*x1 - (8-y1);
            list[position].setColor(status);
        }
    }


    list[64].setColor(oldClr);
}

void Board::display() {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),15);

    int j = 1;
    cout << endl << endl << "\t\t\t";
    for (int i = 1; i <= 8; i++) {
        cout << "  " << i;
    }
    cout << endl << "\t\t\t" << j;
    j++;
    for (int i = 1; i < 65; i++) {
        list[i].display();
        if (i % 8 == 0 && i != 0 && j != 9) {
            cout << endl << "\t\t\t" << j;
            j++;
        }
    }

    blackpiece = 0;
    redpiece = 0;
    for (int i = 1; i < 65; i++) {
        int clr = list[i].getColor();
        if (clr == 0) {
            blackpiece++;
        } else if (clr == 1) {
            redpiece++;
        }
    }

    cout << endl << endl << "\t\t\t   Green: " << blackpiece << endl;
    cout << "\t\t\t   Red: " << redpiece << endl;

    cout << endl << endl << endl;
}

void Board::execute() {
    status = 0; // Green goes first
    winner = 2; // Undecided winner
    redpiece = 2;
    blackpiece = 2;

    blackpiece = 0;
    redpiece = 0;
    for (int i = 1; i < 65; i++) {
        int clr = list[i].getColor();
        if (clr == 0) {
            blackpiece++;
        } else if (clr == 1) {
            redpiece++;
        }
    }

    cout << "\t\t\t   Green: " << blackpiece << endl;
    cout << "\t\t\t   Red: " << redpiece << endl << endl;

    int count = 0;

    while (redpiece != 0 && blackpiece != 0 && (redpiece+blackpiece) != 64) {
        move();

        // Switch turns
        if (status == 0) {
            status++;
        } else {
            status = 0;
        }

        display();
    };

    // Surrender
    if (redpiece == 0 && blackpiece > 0) {
        cout << "GREEN IS THE WINNER!!";
        cout << endl << endl << "GAME OVER.";
        return;
    } else if (blackpiece == 0 && redpiece > 0) {
        cout << "RED IS THE WINNER!!";
        cout << endl << endl << "GAME OVER.";
        return;

    } else if (blackpiece + redpiece == 64) {
        if (blackpiece > redpiece) {
            cout << "GREEN IS THE WINNER!!";
            cout << endl << endl << "GAME OVER.";
            return;

        } else if (redpiece > blackpiece) {
            cout << "RED IS THE WINNER!!";
            cout << endl << endl << "GAME OVER.";
            return;

        } else {
            cout << "Stalemate - It's a tie!!";
            cout << endl << endl << "GAME OVER.";
            return;

        }
    }

}

int main () {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),10);
    cout << endl << "\tWelcome to";
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),12);
    cout << " Holiday Othello";
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),10);
    cout << "! Displaying default game ";
    cout << "board below..." << endl << endl;

    Board othello;

    othello.execute();

    return 0;
}
