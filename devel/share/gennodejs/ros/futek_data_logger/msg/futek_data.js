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

class futek_data {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.futek1 = null;
      this.futek2 = null;
    }
    else {
      if (initObj.hasOwnProperty('futek1')) {
        this.futek1 = initObj.futek1
      }
      else {
        this.futek1 = 0.0;
      }
      if (initObj.hasOwnProperty('futek2')) {
        this.futek2 = initObj.futek2
      }
      else {
        this.futek2 = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type futek_data
    // Serialize message field [futek1]
    bufferOffset = _serializer.float32(obj.futek1, buffer, bufferOffset);
    // Serialize message field [futek2]
    bufferOffset = _serializer.float32(obj.futek2, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type futek_data
    let len;
    let data = new futek_data(null);
    // Deserialize message field [futek1]
    data.futek1 = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [futek2]
    data.futek2 = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'futek_data_logger/futek_data';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0b61dc96ccfbf1e910f406986b9acb9a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 futek1
    float32 futek2
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new futek_data(null);
    if (msg.futek1 !== undefined) {
      resolved.futek1 = msg.futek1;
    }
    else {
      resolved.futek1 = 0.0
    }

    if (msg.futek2 !== undefined) {
      resolved.futek2 = msg.futek2;
    }
    else {
      resolved.futek2 = 0.0
    }

    return resolved;
    }
};

module.exports = futek_data;
