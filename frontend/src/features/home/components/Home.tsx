import "../styles/Home.css";
import Searchbar from "./Searchbar";
import { motion } from "framer-motion";

const initial = {
  translateY: "800px",
};

const animate = {
  translateY: 0,
};

const Home = () => {
  return (
    <div className="home">
      <motion.p
        initial={initial}
        animate={animate}
        transition={{ duration: 1 }}
      >
        GHMA
      </motion.p>
      <Searchbar animation={true} />
    </div>
  );
};

export default Home;
