import React from "react";

export default function Button({ style, title, onClick }) {
  return (
    <button className={style} onClick={onClick}>
      {title}
    </button>
  );
}
