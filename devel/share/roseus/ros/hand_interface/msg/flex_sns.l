;; Auto-generated. Do not edit!


(when (boundp 'hand_interface::flex_sns)
  (if (not (find-package "HAND_INTERFACE"))
    (make-package "HAND_INTERFACE"))
  (shadow 'flex_sns (find-package "HAND_INTERFACE")))
(unless (find-package "HAND_INTERFACE::FLEX_SNS")
  (make-package "HAND_INTERFACE::FLEX_SNS"))

(in-package "ROS")
;;//! \htmlinclude flex_sns.msg.html


(defclass hand_interface::flex_sns
  :super ros::object
  :slots (_curl1 _hype1 _curl2 _hype2 _curl3 _hype3 _curl4 _hype4 ))

(defmethod hand_interface::flex_sns
  (:init
   (&key
    ((:curl1 __curl1) 0)
    ((:hype1 __hype1) 0)
    ((:curl2 __curl2) 0)
    ((:hype2 __hype2) 0)
    ((:curl3 __curl3) 0)
    ((:hype3 __hype3) 0)
    ((:curl4 __curl4) 0)
    ((:hype4 __hype4) 0)
    )
   (send-super :init)
   (setq _curl1 (round __curl1))
   (setq _hype1 (round __hype1))
   (setq _curl2 (round __curl2))
   (setq _hype2 (round __hype2))
   (setq _curl3 (round __curl3))
   (setq _hype3 (round __hype3))
   (setq _curl4 (round __curl4))
   (setq _hype4 (round __hype4))
   self)
  (:curl1
   (&optional __curl1)
   (if __curl1 (setq _curl1 __curl1)) _curl1)
  (:hype1
   (&optional __hype1)
   (if __hype1 (setq _hype1 __hype1)) _hype1)
  (:curl2
   (&optional __curl2)
   (if __curl2 (setq _curl2 __curl2)) _curl2)
  (:hype2
   (&optional __hype2)
   (if __hype2 (setq _hype2 __hype2)) _hype2)
  (:curl3
   (&optional __curl3)
   (if __curl3 (setq _curl3 __curl3)) _curl3)
  (:hype3
   (&optional __hype3)
   (if __hype3 (setq _hype3 __hype3)) _hype3)
  (:curl4
   (&optional __curl4)
   (if __curl4 (setq _curl4 __curl4)) _curl4)
  (:hype4
   (&optional __hype4)
   (if __hype4 (setq _hype4 __hype4)) _hype4)
  (:serialization-length
   ()
   (+
    ;; int32 _curl1
    4
    ;; int32 _hype1
    4
    ;; int32 _curl2
    4
    ;; int32 _hype2
    4
    ;; int32 _curl3
    4
    ;; int32 _hype3
    4
    ;; int32 _curl4
    4
    ;; int32 _hype4
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _curl1
       (write-long _curl1 s)
     ;; int32 _hype1
       (write-long _hype1 s)
     ;; int32 _curl2
       (write-long _curl2 s)
     ;; int32 _hype2
       (write-long _hype2 s)
     ;; int32 _curl3
       (write-long _curl3 s)
     ;; int32 _hype3
       (write-long _hype3 s)
     ;; int32 _curl4
       (write-long _curl4 s)
     ;; int32 _hype4
       (write-long _hype4 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _curl1
     (setq _curl1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _hype1
     (setq _hype1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _curl2
     (setq _curl2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _hype2
     (setq _hype2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _curl3
     (setq _curl3 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _hype3
     (setq _hype3 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _curl4
     (setq _curl4 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _hype4
     (setq _hype4 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get hand_interface::flex_sns :md5sum-) "57e523c8816fb6474dc2708662828753")
(setf (get hand_interface::flex_sns :datatype-) "hand_interface/flex_sns")
(setf (get hand_interface::flex_sns :definition-)
      "int32 curl1
int32 hype1
int32 curl2
int32 hype2
int32 curl3
int32 hype3
int32 curl4
int32 hype4

")



(provide :hand_interface/flex_sns "57e523c8816fb6474dc2708662828753")


