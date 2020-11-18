;; Auto-generated. Do not edit!


(when (boundp 'futek_data_logger::futek_data)
  (if (not (find-package "FUTEK_DATA_LOGGER"))
    (make-package "FUTEK_DATA_LOGGER"))
  (shadow 'futek_data (find-package "FUTEK_DATA_LOGGER")))
(unless (find-package "FUTEK_DATA_LOGGER::FUTEK_DATA")
  (make-package "FUTEK_DATA_LOGGER::FUTEK_DATA"))

(in-package "ROS")
;;//! \htmlinclude futek_data.msg.html


(defclass futek_data_logger::futek_data
  :super ros::object
  :slots (_futek1 _futek2 ))

(defmethod futek_data_logger::futek_data
  (:init
   (&key
    ((:futek1 __futek1) 0.0)
    ((:futek2 __futek2) 0.0)
    )
   (send-super :init)
   (setq _futek1 (float __futek1))
   (setq _futek2 (float __futek2))
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
    ;; float32 _futek1
    4
    ;; float32 _futek2
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _futek1
       (sys::poke _futek1 (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _futek2
       (sys::poke _futek2 (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _futek1
     (setq _futek1 (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _futek2
     (setq _futek2 (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get futek_data_logger::futek_data :md5sum-) "0b61dc96ccfbf1e910f406986b9acb9a")
(setf (get futek_data_logger::futek_data :datatype-) "futek_data_logger/futek_data")
(setf (get futek_data_logger::futek_data :definition-)
      "float32 futek1
float32 futek2

")



(provide :futek_data_logger/futek_data "0b61dc96ccfbf1e910f406986b9acb9a")


