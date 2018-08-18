import Tweet from "./components/Tweet";
class Main extends React.Component {
    render() {
        return (
            <div>
                <Tweet />
            </div>
        );
    }
}
let documentReady = () => {
    ReactDOM.render(
        <Main />,
        document.getElementById('react')
    );
};
$(documentReady);