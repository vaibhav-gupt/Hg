#!/bin/sh 
# -*- scheme -*-
exec guile -e '(@@ (spielfaehig) main)' -s "$0" "$@"
!#

(define-module (spielfaehig)
  #:export (spielfähig main))
(use-modules (srfi srfi-1) ; for iota with count and start
             (ice-9 match))

;; base n!/(n! * (n-k)!) implementation
(define (factorial n)
  (if (zero? n) 1 
      (* n (factorial (1- n)))))

(define (nük n k)
  (if (> k n) 0
      (/ (factorial n) 
         (factorial k) 
         (factorial (- n k)))))

;; optimize nük für small k and huge n
(define (n!/n-k!_reference n k)
  (if (<= k 1) n
      (* (- n (- k 1))
         (n!/n-k! n (- k 1)))))

;; more efficient implementation (tight inner loop)
(define (n!/n-k! n k)
  "(n-k+1) * (n-k+2) * (n-k+...) * n)"
  (if (zero? k) (error "k is 0, but must be > 0")
      (let lp ((k-i (- k 1)))
        (if (zero? k-i) n
            (* (- n k-i)
               (lp (- k-i 1)))))))

(define (nük/small-k n k)
  (if (> k n) 0
      (/ (n!/n-k! n k)
         (factorial k))))

;; binom using the optimized nük
(define (binom p n k)
  (* (nük/small-k n k)
     (expt p k) 
     (expt (- 1 p) (- n k))))

;; the actual interface: probability of having enough people to play at any given gaming night
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

