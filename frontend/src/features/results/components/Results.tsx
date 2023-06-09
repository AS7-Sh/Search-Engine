import Searchbar from "../../home/components/Searchbar";
import "../styles/Results.css";
import "../../home/styles/Home.css";
import Result from "./Result";
import { useSearchParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { SearchResult, getSearchResults } from "../../../api/search";

const Results = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getResults = async () => {
      const results = await getSearchResults(
        searchParams.get("dataset")!,
        searchParams.get("page")!,
        searchParams.get("query")!
      );
      setResults(results);
      setLoading(false);
    };

    getResults();
  }, []);

  const handlePaginate = async (paginate: string) => {
    setLoading(true);
    let newUrl = `/search?dataset=${searchParams.get(
      "dataset"
    )}&query=${searchParams.get("query")}&page=`;

    const page = parseInt(searchParams.get("page")!);
    const nextPage = `${
      paginate === "prev" ? (page === 0 ? 0 : page - 1) : page + 1
    }`;
    navigate(newUrl + nextPage);

    const results = await getSearchResults(
      searchParams.get("dataset")!,
      nextPage,
      searchParams.get("query")!
    );
    setResults(results);
    setLoading(false);
    window.scrollTo({ top: 0, left: 0, behavior: "smooth" });
  };

  const handleChange = async (query: string, dataset: string) => {
    setLoading(true);
    const results = await getSearchResults(dataset, "0", query);
    setResults(results);
    setLoading(false);
    window.scrollTo({ top: 0, left: 0, behavior: "smooth" });
  };

  if (loading)
    return (
      <div className="results results-loader">
        <div className="loader"></div>
      </div>
    );

  return (
    <div className="results">
      <Searchbar
        animation={false}
        defaultValue={searchParams.get("query") || ""}
        defaultDataset={searchParams.get("dataset") || ""}
        handleChange={handleChange}
      />
      {results.map((result, index) => (
        <Result key={index} id={result._id} content={result.content} />
      ))}
      <div className="buttons">
        <button
          onClick={() => handlePaginate("prev")}
          disabled={parseInt(searchParams.get("page")!) === 0}
        >
          Prev
        </button>
        <button onClick={() => handlePaginate("next")}>Next</button>
      </div>
    </div>
  );
};

export default Results;
