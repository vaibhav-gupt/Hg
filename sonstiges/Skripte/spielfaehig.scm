#!/bin/sh 
# -*- scheme -*-
exec guile -e '(@@ (spielfaehig) main)' -s "$0" "$@"
!#

(define-module (spielfaehig)
  #:export (spielfähig main))
(use-modules (srfi srfi-1) ; for iota with count and start
             (ice-9 match))
(define (factorial n)
  (if (zero? n) 1 
      (* n (factorial (1- n)))))

(define (nük n k)
  (if (> k n) 0
      (/ (factorial n) 
         (factorial k) 
         (factorial (- n k)))))

(define (binom p n k)
  (* (nük n k) 
     (expt p k) 
     (expt (- 1 p) (- n k))))

(define (spielfähig p n min_spieler) 
  (apply + 
         (map (lambda (k) (binom p n k)) 
              (iota (1+ (- n min_spieler)) min_spieler))))           


(define (main args)
  (if (match args
             ((script) #t)
             ((arg ...) #f))
      (format #t "~A\n" "Usage: ./spielfaehig.py prob players min_players
    - prob: the probability of each player to take part in the game.
    - players: the total number of players who might take part.
    - min_players: the number of players you need to play. ")
      (let 
          ((prob (inexact->exact (string->number (match args ((script prob N min) prob)))))
           (N (string->number (match args ((script prob N min) N))))
           (min (string->number (match args ((script prob N min) min)))))
        (format #t "~A\n" (exact->inexact (spielfähig prob N min))))))

