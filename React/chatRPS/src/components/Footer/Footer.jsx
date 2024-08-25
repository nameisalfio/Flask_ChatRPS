import ScrollToTop from "react-scroll-to-top";

export function Footer() {

    return (
        <div className="card text-center bg-dark" style={{ width: "100%", margin: "0 auto", color: "white", borderRadius: "0" }}>

            <ScrollToTop smooth />
            <div className="card-header" style={{ borderBottom: "1px solid grey" }}>
                &copy; Copiright - Gabriele Ruggieri & Alfio Spoto
            </div>
            <div className="card-body">
                <h5 className="card-title" style={{ paddingBottom: ".5rem" }}>ChatRPS 2024</h5>
                <p className="card-text">I megghiu</p>
            </div>

        </div>
    );
}