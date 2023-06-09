import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";

interface CustomDropDownProps {
  header: string;
  onSelect: (selected: string) => void;
}

const CustomDropDown = (props: CustomDropDownProps) => {
  return (
    <DropdownButton id="dropdown-basic-button" title={props.header}>
      <Dropdown.Item onClick={() => props.onSelect("Antique")}>
        Antique
      </Dropdown.Item>
      <Dropdown.Item onClick={() => props.onSelect("Wikir")}>
        Wikir
      </Dropdown.Item>
    </DropdownButton>
  );
};

export default CustomDropDown;
