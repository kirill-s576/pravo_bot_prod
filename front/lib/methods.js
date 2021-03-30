export function recursiveSearchById(id, currentNode) {
  let i,
      currentChild,
      result;
  if (id === currentNode.id) {
    return currentNode;
  } else {
    for (i = 0; i < currentNode.children.length; i += 1) {
      currentChild = currentNode.children[i];

      result = recursiveSearchById(id, currentChild);

      if (result !== false) {
        return result;
      }
    }
    return false;
  }
}

export function arraySearchById (id, objectsList) {
  return objectsList.filter(el => el.id === id)
}
