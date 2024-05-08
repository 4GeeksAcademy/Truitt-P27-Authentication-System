import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	useEffect(
		() => {
		if (store.token && store.token != "" && store.token != undefined) actions.getMessage();
	},
	[store.token]);
	
	return (
		<div className="text-center mt-5">
			<h1>Homepage</h1>
			<p>
			</p>
			<div className="alert alert-info">{store.message}
			</div>
			<p>
				This boilerplate comes with lots of documentation:{" "}
				<a href="https://start.4geeksacademy.com/starters/react-flask">
					Read documentation
				</a>
			</p>
		</div>
	);
};
