import { ChangeEvent, useRef, useState } from "react";
import CustomDropDown from "../../../common/components/CustomDropdown";
import { ToastContainer, toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useSearchParams } from "react-router-dom";
import { SearchResult, getQuerySuggestion } from "../../../api/search";

const initial = {
  translateY: "800px",
};

const animate = {
  translateY: 0,
};

interface SearchbarProps {
  animation: boolean;
  defaultValue?: string;
  defaultDataset?: string;
  handleChange?: (query: string, dataset: string) => void;
}

const Searchbar = ({
  animation,
  defaultValue,
  defaultDataset,
  handleChange,
}: SearchbarProps) => {
  const [dataset, setDataset] = useState(defaultDataset || "Dataset");
  const [queries, setQueries] = useState<SearchResult[]>([]);

  const searchRef = useRef<HTMLInputElement>(null);

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const onSelect = (selected: string) => setDataset(selected);

  const handleSearch = () => {
    const query = searchRef.current?.value;
    if (!query) return toast.error("Provide your query ..");
    else if (dataset === "Dataset") return toast.error("Select the dataset ..");

    if (handleChange) {
      navigate(`/search?dataset=${dataset}&query=${query}&page=${0}`);
      handleChange(query, dataset);
    } else
      navigate(
        `/search?dataset=${dataset}&query=${query}&page=${
          searchParams.get("page") || 0
        }`
      );
  };

  const handleQuerySuggestion = async ({
    currentTarget,
  }: ChangeEvent<HTMLInputElement>) => {
    if (dataset !== "Dataset") {
      const results = await getQuerySuggestion(dataset, currentTarget.value);
      setQueries(results);
    }
  };

  const handleChooseQuery = (query: string) => {
    if (searchRef.current) searchRef.current.value = query;
  };

  return (
    <>
      <motion.div
        className={`search-bar ${queries.length !== 0 ? "query-suggest" : ""}`}
        initial={animation ? initial : {}}
        animate={animate}
        transition={{ duration: 1, delay: 0.5 }}
      >
        <ToastContainer />
        <input
          type="search"
          placeholder="Search GHMA .."
          ref={searchRef}
          defaultValue={defaultValue || ""}
          onChange={handleQuerySuggestion}
        />
        <CustomDropDown onSelect={onSelect} header={dataset} />
        <i className="las la-search" onClick={handleSearch} />
      </motion.div>
      <div className="queries">
        {queries.map((query) => (
          <p key={query._id} onClick={() => handleChooseQuery(query.content)}>
            {query.content}
          </p>
        ))}
      </div>
    </>
  );
};

export default Searchbar;
