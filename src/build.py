import fontforge
import psMat
import json
import os
import shutil
import tempfile

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(PROJECT_DIR, "dist")
SRC_DIR = os.path.join(PROJECT_DIR, "src")
DOCS_DIR = os.path.join(PROJECT_DIR, "docs")

os.makedirs(os.path.join(DIST_DIR, "ttf"), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, "otf"), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, "web"), exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# 1. Complete Bengutas Display (Epigraphic Lapidary) Glyphs
bengu_tas_glyphs = {
    "A": ("M 535 800 L 456 595 H 176 L 95 800 H 5 L 280 86 L 310 40 L 340 86 L 625 800 H 535 Z M 310 170 L 426 515 H 206 Z", 633, 65),
    "B": ("M 95 86 H 320 L 410 160 L 450 240 L 410 320 L 330 380 L 425 440 L 470 530 L 425 640 L 330 800 H 95 Z M 183 162 V 340 H 290 L 340 300 L 360 250 L 340 200 L 290 162 Z M 183 416 V 724 H 300 L 355 670 L 380 580 L 355 490 L 300 416 Z", 565, 66),
    "C": ("M 540 230 L 460 245 L 435 180 L 360 140 H 240 L 150 210 L 105 320 L 105 560 L 150 670 L 240 740 H 360 L 435 700 L 460 635 L 540 650 L 505 750 L 400 800 H 210 L 80 710 L 20 570 L 20 310 L 80 170 L 210 86 H 400 L 505 136 Z", 565, 67),
    "Ccedilla": ("M 540 230 L 460 245 L 435 180 L 360 140 H 240 L 150 210 L 105 320 L 105 560 L 150 670 L 240 740 H 360 L 435 700 L 460 635 L 540 650 L 505 750 L 400 800 H 210 L 80 710 L 20 570 L 20 310 L 80 170 L 210 86 H 400 L 505 136 Z M 349 939 q 0 48 -36 74.5 t -108 26.5 q -31 0 -49 -5 v -55 q 9 2 23.5 3.5 t 28 1.5 q 35 0 53.5 -9.5 t 18.5 -34.5 q 0 -26 -26 -38 t -63 -17 l 42 -86 h 56.5 l -25.5 53 q 35 8 60 28 t 25 58 z", 565, 199),
    "D": ("M 95 86 H 310 L 430 180 L 510 310 L 510 570 L 430 700 L 310 800 H 95 Z M 183 162 V 724 H 280 L 370 640 L 425 540 L 425 340 L 370 240 L 280 162 Z", 605, 68),
    "E": ("M 95 86 H 480 L 450 162 H 183 V 400 H 420 L 390 476 H 183 V 724 H 480 L 450 800 H 95 Z", 535, 69),
    "F": ("M 95 86 H 480 L 450 162 H 183 V 400 H 420 L 390 476 H 183 V 800 H 95 Z", 500, 70),
    "G": ("M 540 230 L 460 245 L 435 180 L 360 140 H 240 L 150 210 L 105 320 L 105 560 L 150 670 L 240 740 H 360 L 435 700 V 470 H 290 V 390 H 515 V 740 L 400 800 H 210 L 80 710 L 20 570 L 20 310 L 80 170 L 210 86 H 400 L 505 136 Z", 615, 71),
    "Gbreve": ("M 540 230 L 460 245 L 435 180 L 360 140 H 240 L 150 210 L 105 320 L 105 560 L 150 670 L 240 740 H 360 L 435 700 V 470 H 290 V 390 H 515 V 740 L 400 800 H 210 L 80 710 L 20 570 L 20 310 L 80 170 L 210 86 H 400 L 505 136 Z M 190 -20 L 290 60 L 390 -20 L 420 15 L 290 100 L 160 15 Z", 615, 286),
    "H": ("M 95 86 H 183 V 400 H 450 V 86 H 538 V 800 H 450 V 476 H 183 V 800 H 95 Z", 633, 72),
    "I": ("M 145 86 H 233 V 800 H 145 Z", 379, 73),
    "Idotaccent": ("M 145 86 H 233 V 800 H 145 Z M 189 -40 L 225 0 L 189 40 L 153 0 Z", 379, 304),
    "J": ("M 330 86 H 418 V 640 L 360 740 L 260 800 H 170 L 95 740 L 140 680 L 190 724 H 240 L 300 680 L 330 620 Z", 450, 74),
    "K": ("M 95 86 H 183 V 370 L 410 140 L 464 86 H 580 L 295 385 L 595 730 L 540 800 L 230 460 L 183 510 V 800 H 95 Z", 625, 75),
    "L": ("M 95 86 H 183 V 724 H 480 L 450 800 H 95 Z", 480, 76),
    "M": ("M 95 800 V 140 L 149 86 H 230 L 442 550 L 654 86 H 735 L 789 140 V 800 H 701 V 240 L 480 720 H 404 L 183 240 V 800 Z", 884, 77),
    "N": ("M 95 86 H 183 L 485 640 V 86 H 573 V 800 H 485 L 183 246 V 800 H 95 Z", 668, 78),
    "O": ("M 320 86 H 420 L 560 180 L 650 310 L 650 570 L 560 700 L 420 800 H 320 L 180 700 L 90 570 L 90 310 L 180 180 Z M 340 162 H 400 L 490 235 L 565 340 L 565 540 L 490 645 L 400 724 H 340 L 250 645 L 175 540 L 175 340 L 250 235 Z", 740, 79),
    "Odieresis": ("M 320 86 H 420 L 560 180 L 650 310 L 650 570 L 560 700 L 420 800 H 320 L 180 700 L 90 570 L 90 310 L 180 180 Z M 340 162 H 400 L 490 235 L 565 340 L 565 540 L 490 645 L 400 724 H 340 L 250 645 L 175 540 L 175 340 L 250 235 Z M 270 -40 L 305 0 L 270 40 L 235 0 Z M 470 -40 L 505 0 L 470 40 L 435 0 Z", 740, 214),
    "P": ("M 95 86 H 320 L 420 160 L 465 250 L 420 340 L 320 416 H 183 V 800 H 95 Z M 183 162 V 340 H 290 L 350 295 L 375 250 L 350 205 L 290 162 Z", 560, 80),
    "Q": ("M 702 442 L 670 580 L 570 700 L 430 760 L 290 760 L 150 700 L 50 580 L 20 442 L 50 300 L 150 180 L 290 120 L 430 120 L 570 180 L 670 300 Z M 115 442 L 135 530 L 205 620 L 300 665 L 420 665 L 515 620 L 585 530 L 605 442 L 585 350 L 515 260 L 420 215 L 300 215 L 205 260 L 135 350 Z M 420 560 L 540 680 L 660 800 L 610 800 L 490 680 L 400 590 Z", 750, 81),
    "R": ("M 95 86 H 300 L 430 140 L 485 240 L 440 370 L 340 435 L 560 740 L 515 800 L 260 460 H 183 V 800 H 95 Z M 183 162 V 384 H 270 L 340 340 L 380 270 L 340 200 L 270 162 Z", 640, 82),
    "S": ("M 460 160 L 400 190 L 370 140 L 280 86 H 190 L 110 150 L 75 240 L 110 320 L 190 370 L 370 440 L 440 490 L 475 570 L 440 680 L 350 770 L 240 800 H 140 L 65 730 L 95 650 L 155 695 L 230 724 H 310 L 375 675 L 395 610 L 370 540 L 295 490 L 125 420 L 55 360 L 25 250 L 65 140 L 155 86 H 290 L 390 120 Z", 535, 83),
    "Scedilla": ("M 460 160 L 400 190 L 370 140 L 280 86 H 190 L 110 150 L 75 240 L 110 320 L 190 370 L 370 440 L 440 490 L 475 570 L 440 680 L 350 770 L 240 800 H 140 L 65 730 L 95 650 L 155 695 L 230 724 H 310 L 375 675 L 395 610 L 370 540 L 295 490 L 125 420 L 55 360 L 25 250 L 65 140 L 155 86 H 290 L 390 120 Z M 349 939 q 0 48 -36 74.5 t -108 26.5 q -31 0 -49 -5 v -55 q 9 2 23.5 3.5 t 28 1.5 q 35 0 53.5 -9.5 t 18.5 -34.5 q 0 -26 -26 -38 t -63 -17 l 42 -86 h 56.5 l -25.5 53 q 35 8 60 28 t 25 58 z", 535, 350),
    "T": ("M 60 86 H 580 L 550 162 H 364 V 800 H 276 V 162 H 90 Z", 640, 84),
    "U": ("M 95 86 H 183 V 580 L 225 670 L 320 724 H 400 L 495 670 L 537 580 V 86 H 625 V 610 L 560 720 L 430 800 H 290 L 160 720 L 95 610 Z", 720, 85),
    "Udieresis": ("M 95 86 H 183 V 580 L 225 670 L 320 724 H 400 L 495 670 L 537 580 V 86 H 625 V 610 L 560 720 L 430 800 H 290 L 160 720 L 95 610 Z M 260 -40 L 295 0 L 260 40 L 225 0 Z M 460 -40 L 495 0 L 460 40 L 425 0 Z", 720, 220),
    "V": ("M 40 86 H 145 L 320 670 L 495 86 H 600 L 365 800 H 275 Z", 640, 86),
    "W": ("M 95 86 V 746 L 149 800 H 230 L 442 336 L 654 800 H 735 L 789 746 V 86 H 701 V 646 L 480 166 H 404 L 183 646 V 86 Z", 884, 87),
    "X": ("M 60 86 H 165 L 320 370 L 475 86 H 580 L 380 442 L 595 800 H 490 L 320 514 L 150 800 H 45 L 260 442 Z", 640, 88),
    "Y": ("M 70 86 H 165 L 320 400 L 475 86 H 570 L 364 470 V 800 H 276 V 470 Z", 640, 89),
    "Z": ("M 95 86 H 540 L 505 162 H 220 L 470 670 L 550 724 V 800 H 80 L 115 724 H 425 L 175 216 L 95 162 Z", 625, 90),
}

bengu_tas_digits = {
    "zero": ("M 240 86 H 310 L 440 180 L 510 310 L 510 570 L 440 700 L 310 800 H 240 L 110 700 L 40 570 L 40 310 L 110 180 Z M 250 162 H 300 L 390 235 L 435 340 L 435 540 L 390 645 L 300 724 H 250 L 160 645 L 115 540 L 115 340 L 160 235 Z", 550, 48),
    "one": ("M 170 86 H 295 V 800 H 207 V 175 L 145 220 L 105 165 Z", 400, 49),
    "two": ("M 80 230 L 155 190 L 220 140 H 320 L 410 180 L 445 270 L 405 360 L 180 640 L 180 724 H 455 V 800 H 80 V 710 L 310 420 L 345 350 L 320 235 H 240 L 165 280 Z", 535, 50),
    "three": ("M 80 160 H 420 L 375 235 L 260 360 L 360 400 L 440 480 L 440 620 L 360 740 L 250 800 H 90 L 50 724 L 125 680 L 210 724 H 290 L 350 670 L 350 560 L 280 490 H 180 V 416 L 310 235 H 80 Z", 535, 51),
    "four": ("M 350 86 H 438 V 520 H 510 V 596 H 438 V 800 H 350 V 596 H 50 L 50 520 L 350 86 Z M 165 520 H 350 V 240 Z", 560, 52),
    "five": ("M 95 86 H 430 V 162 H 183 V 370 L 270 340 L 370 370 L 440 450 L 440 620 L 360 740 L 240 800 H 80 L 45 724 L 115 680 L 210 724 H 290 L 350 670 L 350 550 L 290 476 H 180 L 95 440 Z", 535, 53),
    "six": ("M 360 86 L 410 150 L 183 480 L 270 416 H 330 L 430 470 L 475 570 L 440 700 L 330 800 H 220 L 105 710 L 65 570 L 65 440 L 195 240 Z M 240 490 H 290 L 365 540 L 375 620 L 335 710 L 250 724 H 210 L 155 670 L 155 580 Z", 540, 54),
    "seven": ("M 70 86 H 480 L 240 800 H 140 L 370 162 H 70 Z", 550, 55),
    "eight": ("M 240 86 H 300 L 385 140 L 420 220 L 370 310 L 280 370 L 400 440 L 445 540 L 410 680 L 320 800 H 220 L 130 680 L 95 540 L 140 440 L 260 370 L 170 310 L 120 220 L 155 140 Z M 230 162 H 310 L 340 215 L 310 295 L 230 310 L 200 250 Z M 210 440 H 330 L 360 520 L 330 670 L 210 724 L 180 670 L 180 520 Z", 540, 56),
    "nine": ("M 475 360 L 345 560 L 270 584 H 210 L 110 530 L 65 430 L 100 300 L 210 200 H 320 L 435 290 L 475 430 V 560 L 345 760 L 295 700 L 387 520 Z M 300 510 H 250 L 175 460 L 165 380 L 205 290 L 290 276 H 330 L 385 330 L 385 420 Z", 540, 57),
}

lowercase_map = {
    "A": ("a", 97), "B": ("b", 98), "C": ("c", 99), "Ccedilla": ("ccedilla", 231),
    "D": ("d", 100), "E": ("e", 101), "F": ("f", 102), "G": ("g", 103), "Gbreve": ("gbreve", 287),
    "H": ("h", 104), "I": ("dotlessi", 305), "Idotaccent": ("i", 105), "J": ("j", 106),
    "K": ("k", 107), "L": ("l", 108), "M": ("m", 109), "N": ("n", 110),
    "O": ("o", 111), "Odieresis": ("odieresis", 246), "P": ("p", 112), "Q": ("q", 113),
    "R": ("r", 114), "S": ("s", 115), "Scedilla": ("scedilla", 351), "T": ("t", 116),
    "U": ("u", 117), "Udieresis": ("udieresis", 252), "V": ("v", 118), "W": ("w", 119),
    "X": ("x", 120), "Y": ("y", 121), "Z": ("z", 122),
}

# 2. Complete Bengutas Sans (Contemporary Grotesque with Stone-Chiseled Micro-Details)
sans_chiseled_glyphs = {
    "A": ("M 535 800 L 452 580 H 181 L 98 800 H 10 L 285 86 L 316.5 40 L 348 86 L 623 800 H 535 Z M 316.5 175 L 422 505 H 211 Z", 633, 65),
    "C": ("M 500 220 L 435 270 Q 405 210 355 180 Q 305 150 240 150 Q 150 150 95 225 Q 40 300 40 442 Q 40 584 95 659 Q 150 734 240 734 Q 310 734 365 700 Q 415 666 445 605 L 515 650 Q 470 730 400 775 Q 330 820 235 820 Q 115 820 47.5 725 Q -20 630 -20 442 Q -20 254 47.5 159 Q 115 64 235 64 Q 330 64 405 110 Q 465 145 500 220 Z", 616, 67),
    "G": ("M 500 220 L 435 270 Q 405 210 355 180 Q 305 150 240 150 Q 150 150 95 225 Q 40 300 40 442 Q 40 584 95 659 Q 150 734 240 734 Q 325 734 380 695 Q 435 656 455 580 H 260 V 500 H 545 V 650 Q 500 735 415 780 Q 330 820 235 820 Q 115 820 47.5 725 Q -20 630 -20 442 Q -20 254 47.5 159 Q 115 64 235 64 Q 330 64 405 110 Q 465 145 500 220 Z", 710, 71),
    "K": ("M 95 86 H 183 V 400 L 435 150 H 555 L 285 415 L 570 735 L 505 800 L 183 475 V 800 H 95 Z", 614, 75),
    "M": ("M 95 800 V 135 L 144 86 H 225 L 442 530 L 659 86 H 740 L 789 135 V 800 H 701 V 240 L 472 680 H 412 L 183 240 V 800 Z", 884, 77),
    "N": ("M 95 86 H 183 L 485 620 V 86 H 573 V 800 H 485 L 183 260 V 800 H 95 Z", 668, 78),
    "R": ("M 95 86 H 310 Q 410 86 460 135 Q 510 184 510 270 Q 510 345 465 395 Q 420 440 335 450 L 530 735 L 470 800 L 260 475 H 183 V 800 H 95 Z M 183 162 V 400 H 300 Q 365 400 400 365 Q 430 330 430 270 Q 430 210 395 186 Q 360 162 295 162 Z", 641, 82),
    "S": ("M 465 190 L 410 235 Q 380 185 330 160 Q 280 135 220 135 Q 145 135 105 170 Q 65 205 65 260 Q 65 315 110 350 Q 155 385 240 415 Q 350 455 405 505 Q 460 555 460 635 Q 460 725 395 775 Q 330 820 220 820 Q 140 820 80 780 Q 30 745 5 675 L 75 630 Q 95 685 145 715 Q 195 745 255 745 Q 335 745 375 710 Q 415 675 415 625 Q 415 570 370 535 Q 325 500 240 470 Q 130 430 75 380 Q 20 330 20 250 Q 20 160 85 110 Q 150 60 255 60 Q 345 60 410 100 Q 450 130 465 190 Z", 535, 83),
    "V": ("M 40 86 H 145 L 320 680 L 495 86 H 600 L 360 800 H 280 Z", 640, 86),
    "W": ("M 95 86 V 746 L 149 800 H 230 L 442 336 L 654 800 H 735 L 789 746 V 86 H 701 V 646 L 480 166 H 404 L 183 646 V 86 Z", 884, 87),
    "Y": ("M 70 86 H 165 L 320 400 L 475 86 H 570 L 364 470 V 800 H 276 V 470 Z", 640, 89),
    "Ccedilla": ("M 500 220 L 435 270 Q 405 210 355 180 Q 305 150 240 150 Q 150 150 95 225 Q 40 300 40 442 Q 40 584 95 659 Q 150 734 240 734 Q 310 734 365 700 Q 415 666 445 605 L 515 650 Q 470 730 400 775 Q 330 820 235 820 Q 115 820 47.5 725 Q -20 630 -20 442 Q -20 254 47.5 159 Q 115 64 235 64 Q 330 64 405 110 Q 465 145 500 220 Z M 215 830 H 265 L 275 910 L 320 950 L 290 985 L 245 940 L 225 1010 H 185 L 205 910 Z", 616, 199),
    "Scedilla": ("M 465 190 L 410 235 Q 380 185 330 160 Q 280 135 220 135 Q 145 135 105 170 Q 65 205 65 260 Q 65 315 110 350 Q 155 385 240 415 Q 350 455 405 505 Q 460 555 460 635 Q 460 725 395 775 Q 330 820 220 820 Q 140 820 80 780 Q 30 745 5 675 L 75 630 Q 95 685 145 715 Q 195 745 255 745 Q 335 745 375 710 Q 415 675 415 625 Q 415 570 370 535 Q 325 500 240 470 Q 130 430 75 380 Q 20 330 20 250 Q 20 160 85 110 Q 150 60 255 60 Q 345 60 410 100 Q 450 130 465 190 Z M 225 830 H 275 L 285 910 L 330 950 L 300 985 L 255 940 L 235 1010 H 195 L 215 910 Z", 535, 351),
    "Gbreve": ("M 500 220 L 435 270 Q 405 210 355 180 Q 305 150 240 150 Q 150 150 95 225 Q 40 300 40 442 Q 40 584 95 659 Q 150 734 240 734 Q 325 734 380 695 Q 435 656 455 580 H 260 V 500 H 545 V 650 Q 500 735 415 780 Q 330 820 235 820 Q 115 820 47.5 725 Q -20 630 -20 442 Q -20 254 47.5 159 Q 115 64 235 64 Q 330 64 405 110 Q 465 145 500 220 Z M 200 -20 L 355 50 L 510 -20 L 535 20 L 355 100 L 175 20 Z", 710, 286),
    "c": ("M 410 360 L 350 400 Q 330 355 290 330 Q 250 305 200 305 Q 130 305 85 365 Q 40 425 40 535 Q 40 645 85 705 Q 130 765 200 765 Q 255 765 295 735 Q 335 705 355 655 L 420 695 Q 385 765 330 800 Q 270 835 190 835 Q 90 835 35 755 Q -20 675 -20 535 Q -20 395 35 315 Q 90 235 195 235 Q 275 235 335 275 Q 380 305 410 360 Z", 468, 99),
    "e": ("M 245 235 Q 345 235 405 295 Q 465 355 465 470 V 510 H 50 Q 55 645 115 705 Q 170 765 250 765 Q 310 765 360 735 Q 395 710 415 660 L 485 705 Q 450 770 385 805 Q 320 835 245 835 Q 125 835 55 755 Q -15 675 -15 535 Q -15 395 55 315 Q 125 235 245 235 Z M 385 440 Q 380 365 335 325 Q 290 285 245 285 Q 190 285 145 325 Q 100 365 90 440 Z", 550, 101),
    "k": ("M 60 86 H 145 V 470 L 360 250 H 465 L 225 485 L 480 735 L 415 800 L 145 535 V 800 H 60 Z", 500, 107),
    "s": ("M 390 345 L 335 385 Q 315 345 275 325 Q 235 305 190 305 Q 130 305 95 335 Q 60 365 60 410 Q 60 455 100 485 Q 140 515 210 540 Q 305 575 350 615 Q 395 655 395 720 Q 395 790 340 830 Q 285 870 190 870 Q 120 870 65 835 Q 20 805 0 740 L 65 700 Q 80 745 125 770 Q 170 795 220 795 Q 285 795 320 765 Q 355 735 355 695 Q 355 650 315 620 Q 275 590 200 560 Q 110 525 65 485 Q 20 445 20 380 Q 20 305 75 260 Q 130 215 215 215 Q 290 215 345 250 Q 375 275 390 345 Z", 467, 115),
    "r": ("M 60 250 H 140 V 350 Q 175 295 225 265 Q 275 235 340 235 L 360 315 Q 300 315 245 345 Q 190 375 160 435 V 800 H 60 Z", 408, 114),
    "t": ("M 155 150 H 240 V 250 H 350 L 330 325 H 240 V 670 Q 240 735 285 755 Q 320 770 370 750 L 385 825 Q 320 850 250 835 Q 155 810 155 690 V 325 H 70 L 85 250 H 155 Z", 380, 116),
    "z": ("M 40 250 H 390 L 360 325 H 150 L 365 725 H 410 V 800 H 30 L 60 725 H 280 L 75 325 H 40 Z", 450, 122),
    "ccedilla": ("M 410 360 L 350 400 Q 330 355 290 330 Q 250 305 200 305 Q 130 305 85 365 Q 40 425 40 535 Q 40 645 85 705 Q 130 765 200 765 Q 255 765 295 735 Q 335 705 355 655 L 420 695 Q 385 765 330 800 Q 270 835 190 835 Q 90 835 35 755 Q -20 675 -20 535 Q -20 395 35 315 Q 90 235 195 235 Q 275 235 335 275 Q 380 305 410 360 Z M 180 845 H 225 L 235 910 L 275 940 L 250 970 L 210 935 L 195 995 H 160 L 175 910 Z", 468, 231),
    "scedilla": ("M 390 345 L 335 385 Q 315 345 275 325 Q 235 305 190 305 Q 130 305 95 335 Q 60 365 60 410 Q 60 455 100 485 Q 140 515 210 540 Q 305 575 350 615 Q 395 655 395 720 Q 395 790 340 830 Q 285 870 190 870 Q 120 870 65 835 Q 20 805 0 740 L 65 700 Q 80 745 125 770 Q 170 795 220 795 Q 285 795 320 765 Q 355 735 355 695 Q 355 650 315 620 Q 275 590 200 560 Q 110 525 65 485 Q 20 445 20 380 Q 20 305 75 260 Q 130 215 215 215 Q 290 215 345 250 Q 375 275 390 345 Z M 180 880 H 225 L 235 945 L 275 975 L 250 1005 L 210 970 L 195 1030 H 160 L 175 945 Z", 467, 351),
}

NOTDEF_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
  <path d="M 60 100 H 440 V 800 H 60 Z M 110 150 V 750 H 390 V 150 Z" />
</svg>'''

def compile_font(is_display=False, weight_name="Regular", is_bold=False):
    family_core = "Bengutas Display" if is_display else "Bengutas Sans"
    ps_prefix = "BengutasDisplay" if is_display else "BengutasSans"
    
    font = fontforge.font()
    font.fontname = f"{ps_prefix}-{weight_name}"
    font.familyname = family_core
    font.fullname = f"{family_core} {weight_name}"
    font.weight = weight_name
    font.version = "1.002"
    font.copyright = "Copyright (c) 2026 Bengü Taş Type Project. Licensed under the SIL Open Font License, Version 1.1 (Reserved Font Names: 'Bengü Taş', 'Bengutas')."
    
    font.em = 1000
    font.ascent = 800
    font.descent = 200
    
    font.os2_typoascent_add = 0
    font.os2_typodescent_add = 0
    font.hhea_ascent_add = 0
    font.hhea_descent_add = 0
    font.os2_winascent_add = 0
    font.os2_windescent_add = 0
    
    font.os2_typoascent = 800
    font.os2_typodescent = -200
    font.os2_typolinegap = 0
    font.os2_use_typo_metrics = 1
    
    font.hhea_ascent = 800
    font.hhea_descent = -200
    font.hhea_linegap = 0
    
    font.os2_winascent = 950
    font.os2_windescent = 250
    font.os2_weight = 700 if is_bold else 400
    
    temp_dir = tempfile.mkdtemp(prefix="ff_bengutas_")

    try:
        base_json = os.path.join(SRC_DIR, "bold_glyphs.json" if is_bold else "regular_glyphs.json")
        with open(base_json) as f:
            data = json.load(f)
            base_glyphs = data["glyphs"]

        if is_display:
            excluded_unicodes = set([u for _, _, u in bengu_tas_glyphs.values()] + [u for _, _, u in bengu_tas_digits.values()] + [u for _, u in lowercase_map.values()])
            
            for g_item in base_glyphs:
                u = g_item.get("unicode")
                adv = g_item.get("advance", 500)
                d = g_item.get("d")
                if u is None or u in excluded_unicodes:
                    continue
                clean_name = g_item["name"].replace("Regular ", "").replace("Bold ", "").replace(" — Export", "")
                parts = clean_name.split(" ", 1)
                glyph_name = parts[1] if len(parts) > 1 else f"uni{u:04X}"
                if d:
                    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="{d}" /></svg>'
                    svg_p = os.path.join(temp_dir, f"base_{u}.svg")
                    with open(svg_p, "w") as tf: tf.write(svg)
                    g = font.createChar(u, glyph_name)
                    g.importOutlines(svg_p)
                    g.width = adv
                    g.removeOverlap()
                    g.correctDirection()

            for name, (d, adv, u) in bengu_tas_glyphs.items():
                svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="{d}" /></svg>'
                svg_p = os.path.join(temp_dir, f"runic_{name}.svg")
                with open(svg_p, "w") as tf: tf.write(svg)
                g = font.createChar(u, name)
                g.importOutlines(svg_p)
                g.width = adv + (50 if is_bold else 0)
                if is_bold:
                    g.changeWeight(42, "auto", 0, 0, "auto")
                g.removeOverlap()
                g.correctDirection()

            for name, (d, adv, u) in bengu_tas_digits.items():
                svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="{d}" /></svg>'
                svg_p = os.path.join(temp_dir, f"runic_digit_{name}.svg")
                with open(svg_p, "w") as tf: tf.write(svg)
                g = font.createChar(u, name)
                g.importOutlines(svg_p)
                g.width = adv + (40 if is_bold else 0)
                if is_bold:
                    g.changeWeight(42, "auto", 0, 0, "auto")
                g.removeOverlap()
                g.correctDirection()

            for up_name, (low_name, low_u) in lowercase_map.items():
                if up_name in font:
                    g_up = font[up_name]
                    g_low = font.createChar(low_u, low_name)
                    font.selection.select(up_name)
                    font.copy()
                    font.selection.select(low_name)
                    font.paste()
                    g_low.transform(psMat.scale(0.82))
                    g_low.width = int(g_up.width * 0.82)
                    g_low.removeOverlap()
                    g_low.correctDirection()

        else:
            # Sans: Base glyphs + refined stone-chiseled glyphs
            refined_unicodes = set([u for _, _, u in sans_chiseled_glyphs.values()])

            for g_item in base_glyphs:
                u = g_item.get("unicode")
                adv = g_item.get("advance", 500)
                d = g_item.get("d")
                if u is None or not d or u in refined_unicodes:
                    continue
                clean_name = g_item["name"].replace("Regular ", "").replace("Bold ", "").replace(" — Export", "")
                parts = clean_name.split(" ", 1)
                glyph_name = parts[1] if len(parts) > 1 else f"uni{u:04X}"
                svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="{d}" /></svg>'
                svg_p = os.path.join(temp_dir, f"base_sans_{u}.svg")
                with open(svg_p, "w") as tf: tf.write(svg)
                g = font.createChar(u, glyph_name)
                g.importOutlines(svg_p)
                g.width = adv
                g.removeOverlap()
                g.correctDirection()

            for name, (d, adv, u) in sans_chiseled_glyphs.items():
                svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="{d}" /></svg>'
                svg_p = os.path.join(temp_dir, f"chiseled_{name}.svg")
                with open(svg_p, "w") as tf: tf.write(svg)
                g = font.createChar(u, name)
                g.importOutlines(svg_p)
                g.width = adv + (30 if is_bold else 0)
                if is_bold:
                    g.changeWeight(38, "auto", 0, 0, "auto")
                g.removeOverlap()
                g.correctDirection()

        # Space & .notdef
        space_width = 300 if is_bold else 280
        for sp_code in [32, 160]:
            sp = font.createChar(sp_code, "space" if sp_code == 32 else "nbspace")
            sp.width = space_width

        notdef_path = os.path.join(temp_dir, "notdef.svg")
        with open(notdef_path, "w") as tf: tf.write(NOTDEF_SVG)
        notdef = font.createChar(-1, ".notdef")
        notdef.importOutlines(notdef_path)
        notdef.width = 500
        notdef.removeOverlap()
        notdef.correctDirection()

        # Output formats
        ttf_path = os.path.join(DIST_DIR, "ttf", f"{font.fontname}.ttf")
        otf_path = os.path.join(DIST_DIR, "otf", f"{font.fontname}.otf")
        woff_path = os.path.join(DIST_DIR, "web", f"{font.fontname}.woff")
        woff2_path = os.path.join(DIST_DIR, "web", f"{font.fontname}.woff2")
        
        font.generate(ttf_path)
        font.generate(otf_path)
        font.generate(woff_path)
        try: font.generate(woff2_path)
        except: pass

        shutil.copy(woff2_path, os.path.join(DOCS_DIR, f"{font.fontname}.woff2"))
        shutil.copy(ttf_path, os.path.join(DOCS_DIR, f"{font.fontname}.ttf"))

        print(f"✓ Built {font.fontname}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    print("Building full Bengutas font collection...")
    compile_font(is_display=False, weight_name="Regular", is_bold=False)
    compile_font(is_display=False, weight_name="Bold", is_bold=True)
    compile_font(is_display=True, weight_name="Regular", is_bold=False)
    compile_font(is_display=True, weight_name="Bold", is_bold=True)
    print("Complete build finished successfully!")
