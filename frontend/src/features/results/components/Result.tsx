interface ResultProps {
  id: string;
  content: string;
}

const Result = ({ id, content }: ResultProps) => {
  return (
    <div className="result">
      <p>
        <i className="las la-bullseye" /> {id}
      </p>
      <p>{content}</p>
    </div>
  );
};

export default Result;
