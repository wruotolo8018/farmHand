;; Auto-generated. Do not edit!


(when (boundp 'hand_interface::futek_data)
  (if (not (find-package "HAND_INTERFACE"))
    (make-package "HAND_INTERFACE"))
  (shadow 'futek_data (find-package "HAND_INTERFACE")))
(unless (find-package "HAND_INTERFACE::FUTEK_DATA")
  (make-package "HAND_INTERFACE::FUTEK_DATA"))

(in-package "ROS")
;;//! \htmlinclude futek_data.msg.html


(defclass hand_interface::futek_data
  :super ros::object
  :slots (_futek1 _futek2 ))

(defmethod hand_interface::futek_data
  (:init
   (&key
    ((:futek1 __futek1) 0)
    ((:futek2 __futek2) 0)
    )
   (send-super :init)
   (setq _futek1 (round __futek1))
   (setq _futek2 (round __futek2))
   self)
  (:futek1
   (&optional __futek1)
   (if __futek1 (setq _futek1 __futek1)) _futek1)
  (:futek2
   (&optional __futek2)
   (if __futek2 (setq _futek2 __futek2)) _futek2)
  (:serialization-length
   ()
   (+
    ;; int32 _futek1
    4
    ;; int32 _futek2
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _futek1
       (write-long _futek1 s)
     ;; int32 _futek2
       (write-long _futek2 s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _futek1
     (setq _futek1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _futek2
     (setq _futek2 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get hand_interface::futek_data :md5sum-) "bd56bb9649bdacce672aa395f41c39f2")
(setf (get hand_interface::futek_data :datatype-) "hand_interface/futek_data")
(setf (get hand_interface::futek_data :definition-)
      "int32 futek1
int32 futek2

")



(provide :hand_interface/futek_data "bd56bb9649bdacce672aa395f41c39f2")


