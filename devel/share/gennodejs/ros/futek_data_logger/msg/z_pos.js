// Auto-generated. Do not edit!

// (in-package futek_data_logger.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class z_pos {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.z_pos = null;
    }
    else {
      if (initObj.hasOwnProperty('z_pos')) {
        this.z_pos = initObj.z_pos
      }
      else {
        this.z_pos = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type z_pos
    // Serialize message field [z_pos]
    bufferOffset = _serializer.float32(obj.z_pos, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type z_pos
    let len;
    let data = new z_pos(null);
    // Deserialize message field [z_pos]
    data.z_pos = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'futek_data_logger/z_pos';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2b07eb162418378344d3a01a88af5f3c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 z_pos
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new z_pos(null);
    if (msg.z_pos !== undefined) {
      resolved.z_pos = msg.z_pos;
    }
    else {
      resolved.z_pos = 0.0
    }

    return resolved;
    }
};

module.exports = z_pos;
