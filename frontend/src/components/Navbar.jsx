import styles from '../styles/Layout.module.css';
const Navbar = ({ children }) => {
  return (
    <nav className={styles.Navbar}>
      {children}
    </nav>
  );
};
export default Navbar;
