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
  :slots (_prox1 _dist1 _prox2 _dist2 _prox3 _dist3 ))

(defmethod hand_interface::flex_sns
  (:init
   (&key
    ((:prox1 __prox1) 0)
    ((:dist1 __dist1) 0)
    ((:prox2 __prox2) 0)
    ((:dist2 __dist2) 0)
    ((:prox3 __prox3) 0)
    ((:dist3 __dist3) 0)
    )
   (send-super :init)
   (setq _prox1 (round __prox1))
   (setq _dist1 (round __dist1))
   (setq _prox2 (round __prox2))
   (setq _dist2 (round __dist2))
   (setq _prox3 (round __prox3))
   (setq _dist3 (round __dist3))
   self)
  (:prox1
   (&optional __prox1)
   (if __prox1 (setq _prox1 __prox1)) _prox1)
  (:dist1
   (&optional __dist1)
   (if __dist1 (setq _dist1 __dist1)) _dist1)
  (:prox2
   (&optional __prox2)
   (if __prox2 (setq _prox2 __prox2)) _prox2)
  (:dist2
   (&optional __dist2)
   (if __dist2 (setq _dist2 __dist2)) _dist2)
  (:prox3
   (&optional __prox3)
   (if __prox3 (setq _prox3 __prox3)) _prox3)
  (:dist3
   (&optional __dist3)
   (if __dist3 (setq _dist3 __dist3)) _dist3)
  (:serialization-length
   ()
   (+
    ;; int32 _prox1
    4
    ;; int32 _dist1
    4
    ;; int32 _prox2
    4
    ;; int32 _dist2
    4
    ;; int32 _prox3
    4
    ;; int32 _dist3
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _prox1
       (write-long _prox1 s)
     ;; int32 _dist1
       (write-long _dist1 s)
     ;; int32 _prox2
       (write-long _prox2 s)
     ;; int32 _dist2
       (write-long _dist2 s)
     ;; int32 _prox3
       (write-long _prox3 s)
     ;; int32 _dist3
       (write-long _dist3 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _prox1
     (setq _prox1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _dist1
     (setq _dist1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _prox2
     (setq _prox2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _dist2
     (setq _dist2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _prox3
     (setq _prox3 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _dist3
     (setq _dist3 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get hand_interface::flex_sns :md5sum-) "8b57bff00d9b97e6f6a22eb31c6895cc")
(setf (get hand_interface::flex_sns :datatype-) "hand_interface/flex_sns")
(setf (get hand_interface::flex_sns :definition-)
      "int32 prox1
int32 dist1
int32 prox2
int32 dist2
int32 prox3
int32 dist3

")



(provide :hand_interface/flex_sns "8b57bff00d9b97e6f6a22eb31c6895cc")


