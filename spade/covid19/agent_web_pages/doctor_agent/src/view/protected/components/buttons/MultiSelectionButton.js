import React from "react";
import DropdownToggle from "reactstrap/es/DropdownToggle";
import DropdownMenu from "reactstrap/es/DropdownMenu";
import DropdownItem from "reactstrap/es/DropdownItem";
import ButtonDropdown from "reactstrap/es/ButtonDropdown";
import {Button} from "reactstrap";

/** A function to create dropdowns or near buttons depending on how many options are present */
export default function createMultiSelectionButton(
  self,
  options,
  currentSelected,
  changeSelectionFunction,
  dropDownThreshold = 2,
  preprocessingBeforeShowing = (optionText) => optionText,
  id = ""
) {
  const selectorOpen = `${options.join()}_Open_${id}`;
  return options.length > dropDownThreshold ? (
    <ButtonDropdown isOpen={self.state[selectorOpen]}
                    toggle={() => {
                      let newState = {};
                      newState[selectorOpen] = !self.state[selectorOpen];
                      self.setState(newState)
                    }}>
      <DropdownToggle caret>{preprocessingBeforeShowing(currentSelected)}</DropdownToggle>
      <DropdownMenu>
        {
          options.map(option =>
            <DropdownItem key={option} onClick={() => changeSelectionFunction(option)}>
              {preprocessingBeforeShowing(option)}
            </DropdownItem>
          )
        }
      </DropdownMenu>
    </ButtonDropdown>
  ) : (
    options.map(option =>
      <Button key={option} color="outline-secondary" onClick={() => changeSelectionFunction(option)}
              active={currentSelected === option}>{preprocessingBeforeShowing(option)}</Button>
    )
  )
}
